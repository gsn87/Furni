
FREECADPATH_WIN = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
import sys
sys.path.append(FREECADPATH_WIN)

import FreeCAD

LENGTH = 380.
L1 = 160.
L2 = 110.
THICKNESS = 18.
HEIGHT = 500.

# CenterPart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/CenterPart.FCStd")
doc.Sketch.setDatum("Length", L1)
doc.Sketch.setDatum("Width", WIDTH)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", -THICKNESS)
doc.recompute()
doc.save()

# SidePart #
# Set length and width from first Sketch (pad)
doc = FreeCAD.open(u"C:/Users/Guillaume/Desktop/gsn/cad/Furni/trunk/CAD_Stool/SidePart.FCStd")
doc.Sketch.setDatum("Length", LENGTH)
doc.Sketch.setDatum("Width", L2)
# Set thickness from second Sketch001 (pocket)
doc.Sketch001.setDatum("Thickness", THICKNESS)
doc.recompute()
doc.save()



print "done"
