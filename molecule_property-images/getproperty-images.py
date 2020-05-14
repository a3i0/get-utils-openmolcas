from ovito.io import import_file
from ovito.vis import Viewport, OpenGLRenderer, BondsVis
from ovito_user_modifier_VisualiseMoments import VisualiseMoments
from ovito_user_modifier_CreateGoodBonds import CreateCCbonds, CreateCHbonds, CreateDoublebonds, good_ballandstick


import numpy as np


# Import a file. This creates a Pipeline object.
pipeline=import_file('Mol3-s0-b3lyp-aug-cc-pvdz-optim.Opt.xyz')

#Remove simulation cell
# data.cell.vis.enabled=False

# Insert modifiers that operates on the data:
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
vp = Viewport(type=Viewport.Type.Ortho)
vp.zoom_all()
vp.render_image(filename='output.png',size=(1280,720), renderer=OpenGLRenderer())
