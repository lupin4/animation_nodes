import bpy, math
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged
from mn_utils import *
from mn_object_utils import *
from mn_node_helper import *
from mn_cache import *


class SoundInputNode(Node, AnimationNode):
	bl_idname = "SoundInputNode"
	bl_label = "Sound Input"
	
	def getSoundNodesInTree(self, context):
		bakeNodeNames = []
		for node in self.id_data.nodes:
			if node.bl_idname == "SoundBakeNode":
				bakeNodeNames.append((node.name, node.name, ""))
		return bakeNodeNames
		
	bakeNodeName = bpy.props.EnumProperty(items = getSoundNodesInTree, name = "Bake Node", update = nodePropertyChanged)
	
	def init(self, context):
		self.inputs.new("FloatSocket", "Value")
		self.outputs.new("FloatListSocket", "Strengths")
		self.outputs.new("FloatSocket", "Strength")
		
	def getInputSocketNames(self):
		return {"Value" : "value"}
	def getOutputSocketNames(self):
		return {"Strengths" : "strengths",
				"Strength" : "strength"}
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "bakeNodeName", text = "Sound")
		
	def execute(self, value):
		strenghts = []
		bakeNode = self.getBakeNode()
		if bakeNode is not None:
			strenghts = bakeNode.getStrengthListFromCache()
		return strenghts, self.getStrengthOfFrequence(strenghts, value)
		
	def getStrengthOfFrequence(self, strengths, frequenceIndicator):
		if len(strengths) > 0:
			length = len(strengths)
			frequenceIndicator *= length
			lower = strengths[max(min(math.floor(frequenceIndicator), length - 1), 0)]
			upper = strengths[max(min(math.ceil(frequenceIndicator), length - 1), 0)]
			influence = frequenceIndicator % 1.0
			influence = self.interpolation(influence)
			return lower * (1 - influence) + upper * influence
		return 0.0
		
	def interpolation(self, influence):
		influence *= 2
		if influence < 1:
			return influence ** 2 / 2
		else:
			return 1 - (2 - influence) ** 2 / 2
		
	def getBakeNode(self):
		return self.id_data.nodes.get(self.bakeNodeName)
	
		
# register
################################
		
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)