from typing import overload
from typing import TypeVar
from typing import Generic
from .BaseHelper import BaseHelper
from .Pos3D import Pos3D
from .HitResultHelper_Block import HitResultHelper_Block
from .HitResultHelper_Entity import HitResultHelper_Entity

net_minecraft_util_hit_HitResult = TypeVar("net_minecraft_util_hit_HitResult")
HitResult = net_minecraft_util_hit_HitResult

T = TypeVar("T")

class HitResultHelper(Generic[T], BaseHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def resolve(self, hr: HitResult) -> "HitResultHelper":
		pass

	@overload
	def getPos(self) -> Pos3D:
		pass

	@overload
	def asBlock(self) -> HitResultHelper_Block:
		pass

	@overload
	def asEntity(self) -> HitResultHelper_Entity:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


