__author__ = 'GS'

FREECAD_PATH = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
import sys
sys.path.append(FREECAD_PATH)
import FreeCAD
import exportWebGL

DOC_PATH = "C:\Users\Guillaume\Desktop\gsn\cad\Furni\\trunk\CAD_Stool_v1\TestAssemble.FCStd"

doc = FreeCAD.open(DOC_PATH)
stool = [doc.Objects[25]]

exportWebGL.export(stool, './output.html')

print "done"
