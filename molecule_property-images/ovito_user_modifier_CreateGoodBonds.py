from ovito.data import BondType
from ovito.modifiers import CreateBondsModifier
from ovito.vis import BondsVis
import numpy as np

#Defining two bond types with different colours for single and double bonds
Bond1 = BondType(
    id=2,
    name='single',
    color=(0.85,0.85,0.85)
)
Bond2 = BondType(
    id=1,
    name='double',
    color=(0.3,0.3,0.4)
)

def CreateCHbonds(): #returns a modifier
    create_CHbonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
    create_CHbonds.set_pairwise_cutoff('C','H',1.2)
    create_CHbonds.bond_type=Bond1
    create_CHbonds.vis.use_particle_colors=False
    # create_CHbonds.vis.width=0.1

    return create_CHbonds

def CreateCCbonds():
    create_CCbonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise, lower_cutoff=1.4)
    create_CCbonds.set_pairwise_cutoff('C','C',1.6)
    create_CCbonds.bond_type=Bond1
    create_CCbonds.vis.use_particle_colors=False
    # create_CCbonds.vis.width=0.1

    return create_CCbonds

def CreateDoublebonds():
    create_doublebonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
    create_doublebonds.set_pairwise_cutoff('C','O',1.3)
    create_doublebonds.set_pairwise_cutoff('C','C',1.4)
    create_doublebonds.bond_type=Bond2
    create_doublebonds.vis.use_particle_colors=False
    #create_bonds.set_pairwise_cutoff('C','C',1.6)
    # create_doublebonds.vis.width=0.3

    return create_doublebonds


def good_ballandstick(frame,data):
    particle_type=data.particles['Particle Type']

    radius=np.zeros(data.particles.count)
    for i in range(len(particle_type)):
        if(particle_type[i]==1): #This is typically carbon
            radius[i] = 0.3
        if(particle_type[i]==2): #This is typically hydrogen
            radius[i] = 0.2
        if(particle_type[i]==3): #This is typically oxygen
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
