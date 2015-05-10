__author__ = 'GS'

"""FreeCAD webgl exporter

options: importWebGL.wireframeStyle = "faceloop" (can also be "multimaterial" or None)
importWebGL.template = a complete html file, where $CameraData is a placeholder for the
FreeCAD camera, and $ObjectsData a placeholder for the FreeCAD objects.
importWebGL.linewidth = an integer, specifyig the width of lines in "faceloop" mode"""

FREECAD_PATH = "C:\Program Files (x86)\FreeCAD 0.15\\bin"
import sys
sys.path.append(FREECAD_PATH)

DOC_PATH = "C:\Users\GS\Documents\CAD\trunk\CAD_Stool_v1\TestAssemble.FCStd"


import FreeCAD,Draft,Part,DraftGeomUtils

if FreeCAD.GuiUp:
    import FreeCADGui
    from DraftTools import translate
else:
    FreeCADGui = None
    def translate(ctxt,txt):
        return txt

tab = "                " # the tab size
wireframeStyle = "faceloop" # this can be "faceloop", "multimaterial" or None
cameraPosition = None # set this to a tuple to change, for ex. (0,0,0)
linewidth = 1
template = """<!DOCTYPE html>
    <html>
    <head>
        <title>FreeCAD model</title>
        <script src="./js/three.min.js"></script>
        <script src="./js/Detector.js"></script>
        <script src="./js/CanvasRenderer.js"></script>
        <script src="./js/Projector.js"></script>
        <div id="WebGLCanvas">
    </head>
    <body>
        <script>
            // Set up scene and camera
            var scene, camera;

            // x, y and z rotation
            var xRotation = 0.0;
            var yRotation = 0.0;
            var zRotation = 0.0;

            initializeScene();

            animateScene();

            /**
             * Initialze the scene.
             */

            function initializeScene(){
                if(Detector.webgl){
                    renderer = new THREE.WebGLRenderer({antialias:true});
                } else {
                    renderer = new THREE.CanvasRenderer();
                }

                // Set the background color of the renderer to black, with full opacity
                renderer.setClearColor(0x000000, 1);

                // Get the size of the render area
                canvasWidth = 600;
                canvasHeight = 500;

                // Set the renderers size to the content areas size
                renderer.setSize(canvasWidth, canvasHeight);

                // Get the DIV element from the HTML document by its ID and append the renderers DOM
                // object to it
                document.getElementById("WebGLCanvas").appendChild(renderer.domElement);

                scene = new THREE.Scene();

                camera = new THREE.PerspectiveCamera(45, canvasWidth / canvasHeight, 1, 10000);
                camera.position.set(2000, 0, 900);
                camera.lookAt(scene.position);
				camera.rotation.z = 90 * Math.PI / 180;
                scene.add(camera);

				//var axisHelper = new THREE.AxisHelper( 200 );
				//scene.add( axisHelper );

				//placeholder object
				$ObjectsData
				//placeholder object

				var basematerial = new THREE.MeshBasicMaterial( { color: 0xcccccc } );
                stoolMesh = new THREE.Mesh( geom, basematerial );
                scene.add( stoolMesh );

            }

            /**
             * Animate the scene and call rendering.
             */
            function animateScene(){
                // At last, we update the rotation values and assign it to the mesh's rotation.

                // Increase the x, y and z rotation of the cube
                xRotation += 0.03;
                yRotation += 0.02;
                zRotation += 0.04;
				scene.traverse( function( node ) {
					if ( node instanceof THREE.Mesh || node instanceof THREE.Line) {
        // insert your code here, for example:
						node.rotation.z += 0.01
					}
				} );
                //boxMesh.rotation.set(xRotation, yRotation, zRotation);
				//stoolMesh.rotation.y += 0.0
                // Define the function, which is called by the browser supported timer loop. If the
                // browser tab is not visible, the animation is paused. So 'animateScene()' is called
                // in a browser controlled loop.
                requestAnimationFrame(animateScene);

                // Map the 3D scene down to the 2D screen (render the frame)
                renderScene();
            }

            /**
             * Render the scene. Map the 3D world to the 2D screen.
             */
            function renderScene(){
                renderer.render(scene, camera);
            }
        </script>
    </body>
</html>"""


if open.__module__ == '__builtin__':
    pythonopen = open

def export(exportList,filename):
    "exports the given objects to a .html file"

    html = getHTML(exportList)
    outfile = pythonopen(filename,"wb")
    outfile.write(html)
    outfile.close()
    #FreeCAD.Console.PrintMessage(translate("Arch","successfully written ")+filename+"\n")

def getHTML(objectsList):
    "returns the complete HTML code of a viewer for the given objects"

    # get objects data
    objectsData = ''
    for obj in objectsList:
        objectsData += getObjectData(obj)
    #t = template.replace("$CameraData",getCameraData())
    t = template.replace("$ObjectsData",objectsData)
    return t

def getCameraData():
    "returns the position and direction of the camera as three.js snippet"

    result = ""
    if cameraPosition:
        result += "camera.position.set("+str(cameraPosition[0])+","+str(cameraPosition[1])+","+str(cameraPosition[2])+");\n"
    elif FreeCADGui:
        # getting camera position
        pos = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Base
        result += "camera.position.set( "
        result += str(pos.x) + ", "
        result += str(pos.y) + ", "
        result += str(pos.z) + " );\n"
    else:
        result += "camera.position.set(0,0,1000);\n"
    result += tab+"camera.lookAt( scene.position );\n"+tab
    # print result
    return result

def getObjectData(obj,wireframeMode=wireframeStyle):
    """returns the geometry data of an object as three.js snippet. wireframeMode
    can be multimaterial, faceloop or None"""

    result = ""
    wires = []

    if obj.isDerivedFrom("Part::Feature"):
        fcmesh = obj.Shape.tessellate(0.1)
        result = "var geom = new THREE.Geometry();\n"
        # adding vertices data
        for i in range(len(fcmesh[0])):
            v = fcmesh[0][i]
            result += tab+"var v"+str(i)+" = new THREE.Vector3("+str(v.x)+","+str(v.y)+","+str(v.z)+");\n"
        result += tab+"console.log(geom.vertices)\n"
        for i in range(len(fcmesh[0])):
            result += tab+"geom.vertices.push(v"+str(i)+");\n"
        # adding facets data
        for f in fcmesh[1]:
            result += tab+"geom.faces.push( new THREE.Face3"+str(f)+" );\n"
        for f in obj.Shape.Faces:
            for w in f.Wires:
                wo = Part.Wire(DraftGeomUtils.sortEdges(w.Edges))
                wires.append(wo.discretize(QuasiDeflection=0.1))

    elif obj.isDerivedFrom("Mesh::Feature"):
        mesh = obj.Mesh
        result = "var geom = new THREE.Geometry();\n"
        # adding vertices data
        for p in mesh.Points:
            v = p.Vector
            i = p.Index
            result += tab+"var v"+str(i)+" = new THREE.Vector3("+str(v.x)+","+str(v.y)+","+str(v.z)+");\n"
        result += tab+"console.log(geom.vertices)\n"
        for p in mesh.Points:
            result += tab+"geom.vertices.push(v"+str(p.Index)+");\n"
        # adding facets data
        for f in mesh.Facets:
            result += tab+"geom.faces.push( new THREE.Face3"+str(f.PointIndices)+" );\n"

    if result:
        # adding a base material
        if FreeCADGui:
            col = obj.ViewObject.ShapeColor
            rgb = Draft.getrgb(col,testbw=False)
        else:
            rgb = "#888888" # test color
        result += tab+"var basematerial = new THREE.MeshBasicMaterial( { color: 0x"+str(rgb)[1:]+" } );\n"
        #result += tab+"var basematerial = new THREE.MeshLambertMaterial( { color: 0x"+str(rgb)[1:]+" } );\n"

        if wireframeMode == "faceloop":
            # adding the mesh to the scene with a wireframe copy
            result += tab+"var mesh = new THREE.Mesh( geom, basematerial );\n"
            result += tab+"scene.add( mesh );\n"
            result += tab+"var linematerial = new THREE.LineBasicMaterial({linewidth: %d, color: 0x000000,});\n" % linewidth
            for w in wires:
                result += tab+"var wire = new THREE.Geometry();\n"
                for p in w:
                    result += tab+"wire.vertices.push(new THREE.Vector3("
                    result += str(p.x)+", "+str(p.y)+", "+str(p.z)+"));\n"
                result += tab+"var line = new THREE.Line(wire, linematerial);\n"
                result += tab+"scene.add(line);\n"

        elif wireframeMode == "multimaterial":
            # adding a wireframe material
            result += tab+"var wireframe = new THREE.MeshBasicMaterial( { color: "
            result += "0x000000, wireframe: true, transparent: true } );\n"
            result += tab+"var material = [ basematerial, wireframe ];\n"
            result += tab+"var mesh = new THREE.SceneUtils.createMultiMaterialObject( geom, material );\n"
            result += tab+"scene.add( mesh );\n"+tab

        else:
            # adding the mesh to the scene with simple material
            result += tab+"var mesh = new THREE.Mesh( geom, basematerial );\n"
            result += tab+"scene.add( mesh );\n"+tab

    return result

