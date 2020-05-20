#Input: xyz_file.xyz coordinates of particles, rendering method: allowed=opengl and ospray
#Output: xyz_file.png rendered with vectors specified by .raw input files. Vectors scaled to have norm 2.
#Requirements: Python module ovito and ovito pro installed on system.
#              OpenGL rendered requires graphics card, so may not work on remote servers.
#              ovito_user_modifier_VisualiseMoments.py and ovito_user_modifier_CreateGoodBonds.py
#Syntax: python3 getproperty-images.py xyz_file.xyz <rendering method>

from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, OSPRayRenderer
from ovito_user_modifier_VisualiseMoments import VisualiseMoments
from ovito_user_modifier_CreateGoodBonds import CreateCCbonds, CreateCHbonds, CreateDoublebonds, good_ballandstick

import os
import sys
import numpy as np

renderer=sys.argv[1]


#modifier for removing simulation cell
def remove_cell(frame,data):
    data.cell.vis.enabled=False

# Import a file. This creates a Pipeline object.
xyz_file=str(sys.argv[1])
pipeline=import_file(xyz_file)


# Insert modifiers that operates on the data:
pipeline.modifiers.append(remove_cell)
pipeline.modifiers.append(CreateDoublebonds())
pipeline.modifiers.append(CreateCCbonds())
pipeline.modifiers.append(CreateCHbonds())
pipeline.modifiers.append(good_ballandstick)
pipeline.modifiers.append(VisualiseMoments)

#add pipeline to visual scene
pipeline.add_to_scene()
# Compute the effect of the modifiers by evaluating the pipeline.
data=pipeline.compute()
#print("Number of bonds:", data.particles.bonds.count)


#render image
vp = Viewport()
vp.type = Viewport.Type.Ortho
vp.camera_up=(1,0,0)
vp.camera_dir = (1, -1, -0.15)
vp.zoom_all() #note that this resets camera_pos but not camera_dir

osp=OSPRayRenderer()
osp.max_ray_recursion=4

png_file=xyz_file.replace(".xyz" , ".png" )
if (render=='opengl'):
    vp.render_image(filename=png_file,size=(1280,720), alpha=True, renderer=OpenGLRenderer())

if(renderer=='ospray'):
    vp.render_image(filename=png_file,size=(1280,720), alpha=False, renderer=osp)
