from typing import overload
from typing import TypeVar
from .HitResultHelper import HitResultHelper
from .EntityHelper import EntityHelper

net_minecraft_util_hit_EntityHitResult = TypeVar("net_minecraft_util_hit_EntityHitResult")
EntityHitResult = net_minecraft_util_hit_EntityHitResult


class HitResultHelper_Entity(HitResultHelper):

	@overload
	def __init__(self, base: EntityHitResult) -> None:
		pass

	@overload
	def getEntity(self) -> EntityHelper:
		pass

	@overload
	def asEntity(self) -> "HitResultHelper_Entity":
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


