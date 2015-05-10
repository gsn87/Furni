__author__ = 'GS'

FREECAD_PATH = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
import sys
sys.path.append(FREECAD_PATH)
import FreeCAD
import exportWebGL

DOC_PATH = "C:\Users\GS\Documents\CAD\\trunk\OSBTable\OSBTable.FCStd"

doc = FreeCAD.open(DOC_PATH)
stool = [doc.Objects[17]]

exportWebGL.export(stool, './output.html')

print "done"
