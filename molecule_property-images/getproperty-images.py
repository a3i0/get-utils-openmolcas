from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, BondsVis
from ovito_user_modifier_VisualiseMoments import VisualiseMoments
from ovito.modifiers import CreateBondsModifier
from ovito.data import BondType


import numpy as np

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

# Import a file. This creates a Pipeline object.
pipeline=import_file('Mol3-s0-b3lyp-aug-cc-pvdz-optim.Opt.xyz')

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

create_CHbonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
#create_bonds.set_pairwise_cutoff('C','C',1.6)
create_CHbonds.set_pairwise_cutoff('C','H',1.2)
create_CCbonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise, lower_cutoff=1.4)
create_CCbonds.set_pairwise_cutoff('C','C',1.6)
create_doublebonds=CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise)
create_doublebonds.set_pairwise_cutoff('C','O',1.3)
create_doublebonds.set_pairwise_cutoff('C','C',1.4)

create_CHbonds.bond_type=Bond1
create_CCbonds.bond_type=Bond1
create_doublebonds.bond_type=Bond2
create_CHbonds.vis.use_particle_colors=False
create_CHbonds.vis.use_particle_colors=False
create_doublebonds.vis.use_particle_colors=False
# create_CHbonds.vis.width=0.1
# create_doublebonds.vis.width=0.3

# Insert a modifiers that operates on the data:
pipeline.modifiers.append(create_doublebonds)
pipeline.modifiers.append(create_CCbonds)
pipeline.modifiers.append(create_CHbonds)
pipeline.modifiers.append(good_ballandstick)
pipeline.modifiers.append(VisualiseMoments)

pipeline.add_to_scene()
# Compute the effect of the modifiers by evaluating the pipeline.
data=pipeline.compute()
print("Number of bonds:", data.particles.bonds.count)



# types = pipeline.source.data.particles_.particle_types_
# data.particle_types.make_mutable(types)
# types.type_by_name('C').radius = 0.3
# types.type_by_name('H').radius = 0.1
# types.type_by_name('O').radius = 0.4


vp = Viewport(type=Viewport.Type.Ortho)
vp.zoom_all()
vp.render_image(filename='output.png',size=(1280,720), renderer=OpenGLRenderer())
