#Input: dip_len_value.raw, dip_vel_value.raw, mag_value.raw, xyz_file.xyz coordinates of particles
#Output: xyz_file.png rendered with vectors specified by .raw input files.
#Requirements: Python module ovito and ovito installed on system.
#              OpenGL rendered requires graphics card, so may not work on remote servers.
#Syntax: python3 getproperty-images.py xyz_file.xyz

from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, OSPRayRenderer
from ovito_user_modifier_VisualiseMoments import VisualiseMoments
from ovito_user_modifier_CreateGoodBonds import CreateCCbonds, CreateCHbonds, CreateDoublebonds, good_ballandstick

import os
import sys
import numpy as np


dip_len_value=np.loadtxt('dip_len_value.raw')
dip_vel_value=np.loadtxt('dip_vel_value.raw')
mag_value=np.loadtxt('mag_value.raw')

#scaling all values so that their norms are sqrt(2)
dip_len_value= (np.sqrt(2)/np.linalg.norm(dip_len_value))*dip_len_value
dip_vel_value= (np.sqrt(2)/np.linalg.norm(dip_vel_value))*dip_vel_value
mag_value= (np.sqrt(2)/np.linalg.norm(mag_value))*mag_value

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

png_file=xyz_file+str.replace('.xyz','.png')
#vp.render_image(filename='output.png',size=(1280,720), alpha=True, renderer=OpenGLRenderer())
vp.render_image(filename='output.png',size=(1280,720), renderer=OpenGLRenderer()) #opengl without transparency
#vp.render_image(filename='output.png',size=(1280,720), alpha=true, renderer=osp) #Raytraced OSPRayRenderer
