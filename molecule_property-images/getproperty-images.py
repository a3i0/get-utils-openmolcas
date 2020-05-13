import ovito
from ovito_user_modifier_VisualiseMoments import VisualiseMoments


ovito.io.import_file('Mol3-s0-b3lyp-aug-cc-pvdz-optim.Opt.xyz')
ovito.pipeline.modifiers.append(VisualiseMoments)

ovito.pipeline.compute()
