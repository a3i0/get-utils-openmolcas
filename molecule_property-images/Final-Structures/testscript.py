from ovito.data import *
from ovito.vis import VectorVis
from ovito.vis import ParticlesVis
import numpy as np

vector_vis = VectorVis(
    alignment = VectorVis.Alignment.Base, 
    color = (1.0, 0.0, 0.4),
    width = 0.05 )

#transparency_vis = ParticlesVis(
#    transparency=0.1 )

    
def modify(frame, data):
    
    # This user-defined modifier function gets automatically called by OVITO whenever the data pipeline is newly computed.
    # It receives two arguments from the pipeline system:
    # 
    #    frame - The current animation frame number at which the pipeline is being evaluated.
    #    data   - The DataCollection passed in from the pipeline system. 
    #                The function may modify the data stored in this DataCollection as needed.
    # 
    # What follows is an example code snippet doing nothing except printing the current 
    # list of particle properties to the log window. Use it as a starting point for developing 
    # your own data modification or analysis functions. 
    
    
            
    
    
    pos=np.array(data.particles['Position'])
    com=sum(pos)/data.particles.count
    com_repeated=np.tensordot(np.ones(data.particles.count),com,axes=0)
    prop_com = data.particles_.create_property('Centre of Mass', data=com_repeated, components=3)
    
    com_as_particle_index=data.particles_.create_particle(com)
    print(com)
    transparency=np.zeros(data.particles.count)
    transparency[com_as_particle_index]=1
    prop_transparency = data.particles_.create_property('Transparency', data=transparency)
    
    testvector=np.zeros(shape=(data.particles.count,3))
    testvector[com_as_particle_index]=[1,1,1]
    my_prop = data.particles_.create_property('My Property', data=testvector,components=3)
    my_prop.vis = vector_vis
    
    if data.particles != None:
        print("There are %i particles with the following properties:" % data.particles.count)
        for property_name in data.particles.keys():
            print("  '%s'" % property_name)