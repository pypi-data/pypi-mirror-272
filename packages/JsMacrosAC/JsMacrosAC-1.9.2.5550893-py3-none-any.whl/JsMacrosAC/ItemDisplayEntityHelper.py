from typing import overload
from typing import TypeVar
from .DisplayEntityHelper import DisplayEntityHelper
from .ItemStackHelper import ItemStackHelper

net_minecraft_entity_decoration_DisplayEntity_ItemDisplayEntity = TypeVar("net_minecraft_entity_decoration_DisplayEntity_ItemDisplayEntity")
DisplayEntity_ItemDisplayEntity = net_minecraft_entity_decoration_DisplayEntity_ItemDisplayEntity


class ItemDisplayEntityHelper(DisplayEntityHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: DisplayEntity_ItemDisplayEntity) -> None:
		pass

	@overload
	def getItem(self) -> ItemStackHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getTransform(self) -> str:
		"""
		Since: 1.9.1 

		Returns:
			"none", "thirdperson_lefthand", "thirdperson_righthand", "firstperson_lefthand",
        "firstperson_righthand", "head", "gui", "ground" or "fixed" 
		"""
		pass

	pass


