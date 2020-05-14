from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, BondsVis
from ovito_user_modifier_VisualiseMoments import VisualiseMoments
from ovito_user_modifier_CreateGoodBonds import CreateCCbonds, CreateCHbonds, CreateDoublebonds, good_ballandstick


import numpy as np

#modifier for removing simulation cell
def remove_cell(frame,data):
    data.cell.vis.enabled=False

# Import a file. This creates a Pipeline object.
pipeline=import_file('Mol3-s0-b3lyp-aug-cc-pvdz-optim.Opt.xyz')


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


#vp.render_image(filename='output.png',size=(1280,720), alpha=True, renderer=OpenGLRenderer())
vp.render_image(filename='output.png',size=(1280,720), renderer=OpenGLRenderer())
