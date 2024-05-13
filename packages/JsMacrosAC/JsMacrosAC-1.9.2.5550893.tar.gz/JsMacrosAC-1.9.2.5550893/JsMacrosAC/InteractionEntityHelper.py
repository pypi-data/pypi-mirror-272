from typing import overload
from typing import TypeVar
from .EntityHelper import EntityHelper

net_minecraft_entity_decoration_InteractionEntity = TypeVar("net_minecraft_entity_decoration_InteractionEntity")
InteractionEntity = net_minecraft_entity_decoration_InteractionEntity


class InteractionEntityHelper(EntityHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: InteractionEntity) -> None:
		pass

	@overload
	def setCanHit(self, value: bool) -> None:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLastAttacker(self) -> EntityHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLastInteracted(self) -> EntityHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getWidth(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getHeight(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def shouldRespond(self) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


