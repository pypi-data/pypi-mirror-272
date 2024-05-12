from typing import overload
from typing import TypeVar
from .DisplayEntityHelper import DisplayEntityHelper
from .TextDisplayEntityHelper_TextDisplayDataHelper import TextDisplayEntityHelper_TextDisplayDataHelper

net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity = TypeVar("net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity")
DisplayEntity_TextDisplayEntity = net_minecraft_entity_decoration_DisplayEntity_TextDisplayEntity


class TextDisplayEntityHelper(DisplayEntityHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: DisplayEntity_TextDisplayEntity) -> None:
		pass

	@overload
	def getData(self) -> TextDisplayEntityHelper_TextDisplayDataHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


