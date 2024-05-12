from typing import overload
from typing import TypeVar
from .HitResultHelper import HitResultHelper
from .DirectionHelper import DirectionHelper
from .BlockPosHelper import BlockPosHelper

net_minecraft_util_hit_BlockHitResult = TypeVar("net_minecraft_util_hit_BlockHitResult")
BlockHitResult = net_minecraft_util_hit_BlockHitResult


class HitResultHelper_Block(HitResultHelper):

	@overload
	def __init__(self, base: BlockHitResult) -> None:
		pass

	@overload
	def getSide(self) -> DirectionHelper:
		pass

	@overload
	def getBlockPos(self) -> BlockPosHelper:
		pass

	@overload
	def isMissed(self) -> bool:
		pass

	@overload
	def isInsideBlock(self) -> bool:
		pass

	@overload
	def asBlock(self) -> "HitResultHelper_Block":
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


