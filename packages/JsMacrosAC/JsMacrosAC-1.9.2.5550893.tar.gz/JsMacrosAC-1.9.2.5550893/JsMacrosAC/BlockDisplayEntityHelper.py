from typing import overload
from typing import TypeVar
from .DisplayEntityHelper import DisplayEntityHelper
from .BlockStateHelper import BlockStateHelper

net_minecraft_entity_decoration_DisplayEntity_BlockDisplayEntity = TypeVar("net_minecraft_entity_decoration_DisplayEntity_BlockDisplayEntity")
DisplayEntity_BlockDisplayEntity = net_minecraft_entity_decoration_DisplayEntity_BlockDisplayEntity


class BlockDisplayEntityHelper(DisplayEntityHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: DisplayEntity_BlockDisplayEntity) -> None:
		pass

	@overload
	def getBlockState(self) -> BlockStateHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


