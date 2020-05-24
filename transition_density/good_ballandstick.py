from ovito.data import BondType
from ovito.modifiers import CreateBondsModifier
from ovito.vis import BondsVis
import numpy as np

def good_ballandstick(frame,data):
    particle_type=data.particles['Particle Type']

    radius=np.zeros(data.particles.count)
    for i in range(len(particle_type)):
        if(particle_type[i]==6): #Carbon
            radius[i] = 0.3
        if(particle_type[i]==1): #Hydrogen
            radius[i] = 0.2
        if(particle_type[i]==8): #Oxygen
            radius[i] = 0.3

    radius_prop=data.particles_.create_property('Radius', data=radius)

    #data.particles.bonds.vis.enabled = True
    #data.particles.bonds.vis.shading = BondsVis.Shading.Flat
    data.particles.bonds.vis.width = 0.2
    # print(data.particles_.bonds_.bond_types_.type_by_id(2).color)

    # types = pipeline.source.data.particles_.particle_types_
    # data.particle_types.make_mutable(types)
    # types.type_by_name('C').radius = 0.3
    # types.type_by_name('H').radius = 0.1
    # types.type_by_name('O').radius = 0.4
