
FREECADPATH_WIN = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
import sys
sys.path.append(FREECADPATH_WIN)

import FreeCAD

# Dimensions in mm
LENGTH = 300. #length of CenterPart & SideParts
L1 = 200. #width of CenterPart
L2 = 110. #width of SidePart
THICKNESS = 18. #thikness of material
HEIGHT = 800. #height of stool
GAP = 10. #free gap between CenterPart & SidePart

# CenterPart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/CenterPart.FCStd")
doc.Sketch.setDatum("Length", LENGTH)
doc.Sketch.setDatum("Width", L1)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", -THICKNESS)
for obj in doc.Objects:
 obj.touch()
doc.recompute()
doc.save()

# SidePart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/SidePart.FCStd")
doc.Sketch.setDatum("Length", LENGTH)
doc.Sketch.setDatum("Width", -L2)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", THICKNESS)
doc.recompute()
doc.save()

# LinkPart #
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/LinkPart.FCStd")
doc.Sketch.setDatum("Length", x = GAP + L1/2. -30.)
doc.recompute()
doc.save()

# LegPart #
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/LegPart.FCStd")
doc.Sketch.setDatum("Height", -HEIGHT)
doc.Sketch.setDatum("Length", LENGTH-110.)
doc.Sketch001.setDatum("Thickness", THICKNESS)
doc.recompute()
doc.save()






print "done"
