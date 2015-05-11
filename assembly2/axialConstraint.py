from assembly2lib import *
from assembly2lib import __dir__, wb_globals #variables not imported * directive ...
from lib3D import *
from pivy import coin
from PySide import QtGui

class AxialSelectionGate:
     def allow(self, doc, obj, sub):
          if sub.startswith('Face'):
               face = getObjectFaceFromName( obj, sub)
               return hasattr( face.Surface, 'Radius' )
          elif sub.startswith('Edge'):
               edge = getObjectEdgeFromName( obj, sub)
               return isinstance(edge.Curve, Part.Line)
               #return str(edge.Curve).startswith('<Line')
          else:
               return False

def parseSelection(selection, objectToUpdate=None):
     validSelection = False
     if len(selection) == 2:
          s1, s2 = selection
          if s1.ObjectName <> s2.ObjectName:
               if (cylindricalPlaneSelected(s1) or LinearEdgeSelected(s1)) \
                        and (cylindricalPlaneSelected(s2) or LinearEdgeSelected(s2)):
                    validSelection = True
                    cParms = [ [s1.ObjectName, s1.SubElementNames[0] ],
                               [s2.ObjectName, s2.SubElementNames[0] ] ]
     if not validSelection:
          msg = '''To add an axial constraint select two cylindrical surfaces or two straight lines, each from a different part. Selection made:
%s'''  % printSelection(selection)
          QtGui.QMessageBox.information(  QtGui.qApp.activeWindow(), "Incorrect Usage", msg)
          return 

     if objectToUpdate == None:
          cName = findUnusedObjectName('axialConstraint')
          debugPrint(2, "creating %s" % cName )
          c = FreeCAD.ActiveDocument.addObject("App::FeaturePython", cName)
          c.addProperty("App::PropertyString","Type","ConstraintInfo","Object 1").Type = 'axial'
          c.addProperty("App::PropertyString","Object1","ConstraintInfo")
          c.addProperty("App::PropertyString","SubElement1","ConstraintInfo")
          c.addProperty("App::PropertyString","Object2","ConstraintInfo")
          c.addProperty("App::PropertyString","SubElement2","ConstraintInfo")
     
          c.addProperty("App::PropertyEnumeration","directionConstraint", "ConstraintInfo")
          c.directionConstraint = ["none","aligned","opposed"]
                         
          c.setEditorMode('Type',1)
          for prop in ["Object1","Object2","SubElement1","SubElement2"]:
               c.setEditorMode(prop, 1) 

          c.Proxy = ConstraintObjectProxy()
     else:
          debugPrint(2, "redefining %s" % objectToUpdate.Name )
          c = objectToUpdate
          updateObjectProperties(c)

     c.Object1 = cParms[0][0]
     c.SubElement1 = cParms[0][1]
     c.Object2 = cParms[1][0]
     c.SubElement2 = cParms[1][1]

     c.Proxy.callSolveConstraints()
         
class AxialConstraintCommand:
     def Activated(self):
          selection = FreeCADGui.Selection.getSelectionEx()
          if len(selection) == 2:
               parseSelection( selection )
          else:
               FreeCADGui.Selection.clearSelection()
               if wb_globals.has_key('selectionObserver'): 
                    wb_globals['selectionObserver'].stopSelectionObservation()
               wb_globals['selectionObserver'] =  ConstraintSelectionObserver( AxialSelectionGate(), parseSelection  )
     def GetResources(self): 
          return {
               'Pixmap' : os.path.join( __dir__ , 'axialConstraint.svg' ) , 
               'MenuText': 'Add Axial Constraint', 
               'ToolTip': 'Add an Axial Constraint between two objects'
               } 

FreeCADGui.addCommand('addAxialConstraint', AxialConstraintCommand())

class RedefineConstraintCommand:
    def Activated(self):
        self.constObject = FreeCADGui.Selection.getSelectionEx()[0].Object
        debugPrint(3,'redefining %s' % self.constObject.Name)
        FreeCADGui.Selection.clearSelection()
        if wb_globals.has_key('selectionObserver'): 
            wb_globals['selectionObserver'].stopSelectionObservation()
        wb_globals['selectionObserver'] =  ConstraintSelectionObserver( AxialSelectionGate(), self.UpdateConstraint  )
    def UpdateConstraint(self, selection):
        parseSelection( selection, self.constObject)
    def GetResources(self): 
        return { 'MenuText': 'Redefine' } 
FreeCADGui.addCommand('redefineAxialConstraint', RedefineConstraintCommand())
