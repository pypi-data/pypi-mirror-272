from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity_Data = TypeVar("net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity_Data")
DisplayEntity_TextDisplayEntity_Data = net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity_Data


class TextDisplayEntityHelper_TextDisplayDataHelper(BaseHelper):

	@overload
	def __init__(self, base: DisplayEntity_TextDisplayEntity_Data) -> None:
		pass

	@overload
	def getText(self) -> TextHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLineWidth(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getTextOpacity(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getBackgroundColor(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def hasShadowFlag(self) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def hasSeeThroughFlag(self) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def hasDefaultBackgroundFlag(self) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getAlignment(self) -> str:
		"""
		Since: 1.9.1 

		Returns:
			"center", "left" or "right" 
		"""
		pass

	pass


