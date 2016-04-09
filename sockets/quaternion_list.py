import bpy
from .. base_types.socket import AnimationNodeSocket

class QuaternionListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_QuaternionListSocket"
    bl_label = "Quaternion List Socket"
    dataType = "Quaternion List"
    allowedInputTypes = ["Quaternion List"]
    drawColor = (0.8, 0.6, 0.3, 0.5)
    storable = True
    comparable = False

    def getValueCode(self):
        return "[]"

    @classmethod
    def getCopyExpression(cls):
        return "[element.copy() for element in value]"
