
#Syntax: python3 create_transitiondensity.py <cube file> <rendering method> camera_x camera_y camera_z
import os
import sys
import numpy as np

sys.path.append('./../molecule_property-images/') #To import ovito_user_modifier_CreateGoodBonds.py

from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, OSPRayRenderer
from ovito_user_modifier_CreateGoodBonds import CreateCCbonds, CreateCHbonds, CreateDoublebonds
from good_ballandstick import good_ballandstick
from ovito.modifiers import CreateIsosurfaceModifier





cube_file=sys.argv[1]
renderer=sys.argv[2]
camera_dir_x=float(sys.argv[3])
camera_dir_y=float(sys.argv[4])
camera_dir_z=float(sys.argv[5])

#modifier for removing visual element of simulation cell
def remove_cell(frame,data):
    data.cell.vis.enabled=False

pipeline=import_file(cube_file)

#Define two modifiers for creatinf the positive and negative valued isosurfaces
PositiveIsosurfaceModifier=CreateIsosurfaceModifier(
    operate_on='voxels:imported', #default name of imported voxel grids
    property='Property', #default name of scalar voxel data stored in cube files. Source: Ovito GUI when using CreateIsosurfaceModifier on a loaded cube file
    isolevel=0.003
)

NegativeIsosurfaceModifier=CreateIsosurfaceModifier(
    operate_on='voxels:imported',
    property='Property',
    isolevel=-0.003
)
#Visual properties of the isosurface
PositiveIsosurfaceModifier.vis.surface_color=(20.0/256 , 118.0/256 , 223.0/256)
PositiveIsosurfaceModifier.vis.surface_transparency=0.4
PositiveIsosurfaceModifier.vis.show_cap=False
NegativeIsosurfaceModifier.vis.surface_color=(250.0/256 , 235.0/256 , 7.0/256)
NegativeIsosurfaceModifier.vis.surface_transparency=0.4
NegativeIsosurfaceModifier.vis.show_cap=False


# Insert modifiers that operates on the data:
pipeline.modifiers.append(remove_cell)
pipeline.modifiers.append(CreateDoublebonds())
pipeline.modifiers.append(CreateCCbonds())
pipeline.modifiers.append(CreateCHbonds())
pipeline.modifiers.append(good_ballandstick)
pipeline.modifiers.append(PositiveIsosurfaceModifier)
pipeline.modifiers.append(NegativeIsosurfaceModifier)


#add pipeline to visual scene
pipeline.add_to_scene()
# Compute the effect of the modifiers by evaluating the pipeline.
data=pipeline.compute()


#Render
vp = Viewport()
vp.type = Viewport.Type.Perspective
vp.camera_up=(1,0,0)
vp.camera_dir = (camera_dir_x, camera_dir_y, camera_dir_z)
vp.zoom_all() #note that this resets camera_pos but not camera_dir

osp=OSPRayRenderer()
osp.max_ray_recursion=32
osp.refinement_iterations=32
osp.samples_per_pixel=2

if((renderer != "opengl")and(renderer != "ospray")):
    print("Renderer not supported! New image will not be rendered")

png_file="transition_density.png"
if (renderer=="opengl"):
    vp.render_image(filename=png_file,size=(1024,768), alpha=True, renderer=OpenGLRenderer())

if(renderer=="ospray"):
    vp.render_image(filename=png_file,size=(1024,768), alpha=True, renderer=osp)
