from typing import overload
from typing import Mapping
from .EventFilterer import EventFilterer
from .BlockPosHelper import BlockPosHelper
from .BaseEvent import BaseEvent


class FiltererBlockUpdate(EventFilterer):
	"""
	Since: 1.9.1 
	"""
	pos: BlockPosHelper
	pos2: BlockPosHelper
	blockId: str
	blockState: Mapping[str, str]
	updateType: str

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, baseEvent: BaseEvent) -> bool:
		pass

	@overload
	def setPos(self, x: int, y: int, z: int) -> "FiltererBlockUpdate":
		pass

	@overload
	def setPos(self, pos: BlockPosHelper) -> "FiltererBlockUpdate":
		pass

	@overload
	def setArea(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> "FiltererBlockUpdate":
		pass

	@overload
	def setArea(self, pos1: BlockPosHelper, pos2: BlockPosHelper) -> "FiltererBlockUpdate":
		pass

	@overload
	def setBlockId(self, id: str) -> "FiltererBlockUpdate":
		pass

	@overload
	def setUpdateType(self, type: str) -> "FiltererBlockUpdate":
		pass

	@overload
	def setBlockStates(self, states: Mapping[str, str]) -> "FiltererBlockUpdate":
		pass

	@overload
	def setBlockState(self, property: str, value: str) -> "FiltererBlockUpdate":
		"""

		Args:
			value: setting to null will make sure the block doesn't have this property 
		"""
		pass

	pass


