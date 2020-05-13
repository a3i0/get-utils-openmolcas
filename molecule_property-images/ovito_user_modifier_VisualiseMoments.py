from ovito.data import *
from ovito.vis import VectorVis
from ovito.vis import ParticlesVis
import numpy as np

dip_len_vis = VectorVis( #vector visual element that needs to be attached to the relevant property
    alignment = VectorVis.Alignment.Base,
    color = (1.0, 0.0, 0.0),
    width = 0.05 )

dip_vel_vis = VectorVis( #vector visual element that needs to be attached to the relevant property
    alignment = VectorVis.Alignment.Base,
    color = (0.9, 0.4, 0.0),
    width = 0.05 )

mag_vis = VectorVis( #vector visual element that needs to be attached to the relevant property
    alignment = VectorVis.Alignment.Base,
    color = (0.0, 0.0, 1.0),
    width = 0.05 )

def VisualiseMoments(frame, data):

    pos=np.array(data.particles['Position'])
    com=sum(pos)/data.particles.count #centre of mass
    com_repeated=np.tensordot(np.ones(data.particles.count),com,axes=0) #formatting so that the array passed to create_property is of correct dimensions '(Nx3)'
    prop_com = data.particles_.create_property('Centre of Mass', data=com_repeated, components=3)

    com_as_particle_index = data.particles_.create_particle(com) #adds com as a particle and returns its index
    transparency = np.zeros(data.particles.count)
    transparency[com_as_particle_index]=1 #com particle fully transparent
    data.particles_.create_property('Transparency', data=transparency)

    #Adding Dipole in Length gauge
    dip_len=np.zeros(shape=(data.particles.count,3))
    dip_len[com_as_particle_index]=[3,0,0] #value of the dipole that will be rendered only at the com particle
    dip_len_prop = data.particles_.create_property('Dipole Length Gauge', data=dip_len, components=3)
    dip_len_prop.vis = dip_len_vis

    #Adding Dipole in Velocity gauge
    dip_vel=np.zeros(shape=(data.particles.count,3))
    dip_vel[com_as_particle_index]=[0,3,0] #value of the dipole that will be rendered only at the com particle
    dip_vel_prop = data.particles_.create_property('Dipole Velocity Gauge', data=dip_vel, components=3)
    dip_vel_prop.vis = dip_vel_vis

    #Adding magnetic dipole
    mag=np.zeros(shape=(data.particles.count,3))
    mag[com_as_particle_index]=[0,0,3] #value of the dipole that will be rendered only at the com particle
    mag_prop = data.particles_.create_property('Magnetic Dipole', data=mag, components=3)
    mag_prop.vis = mag_vis
