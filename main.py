
FREECADPATH_WIN = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
ASSEMBLY2 = "C:\Users\Guillaume\Desktop\gsn\cad\Furni\\trunk\FreeCAD_assembly2-master"
import sys
sys.path.append(FREECADPATH_WIN)
sys.path.append(ASSEMBLY2)

import FreeCAD
from assembly2solver import solveConstraints
from importPart import importPart

# Dimensions in mm
LENGTH = 370. #length of CenterPart & SideParts
L1 = 160. #width of CenterPart
L2 = 110. #width of SidePart
THICKNESS = 18. #thikness of material
HEIGHT = 430. #height of stool
GAP = 10. #free gap between CenterPart & SidePart

# CenterPart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool_v1/CenterPart.FCStd")
doc.Sketch.setDatum("Length", LENGTH)
doc.Sketch.setDatum("Width", L1)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", -THICKNESS)
doc.recompute()
doc.save()

# SidePart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool_v1/SidePart.FCStd")
doc.Sketch.setDatum("Length", LENGTH)
doc.Sketch.setDatum("Width", -L2)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", THICKNESS)
doc.recompute()
doc.save()

# LinkPart #
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool_v1/LinkPart.FCStd")
doc.Sketch.setDatum("Length", GAP + L1/2. -30.)
doc.recompute()
doc.save()

# LegPart #
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool_v1/LegPart.FCStd")
doc.Sketch.setDatum("Height", -HEIGHT)
doc.Sketch.setDatum("Length", LENGTH-110.)
#doc.Sketch001.setDatum("Thickness", THICKNESS)
doc.recompute()
doc.save()

doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool_v1/TestAssemble.FCStd")
update_part = {}
for obj in doc.Objects:
    if obj.TypeId == 'Part::FeaturePython' and hasattr(obj,"sourceFile"):
        importPart(obj.sourceFile, obj.Label)
doc.recompute()
doc.save()

#solveConstraints(doc)


print "done"
