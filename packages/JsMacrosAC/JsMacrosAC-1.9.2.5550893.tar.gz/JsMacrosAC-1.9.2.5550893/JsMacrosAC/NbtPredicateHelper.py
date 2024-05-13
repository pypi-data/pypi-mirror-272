from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .EntityHelper import EntityHelper
from .ItemStackHelper import ItemStackHelper
from .NBTElementHelper import NBTElementHelper

net_minecraft_predicate_NbtPredicate = TypeVar("net_minecraft_predicate_NbtPredicate")
NbtPredicate = net_minecraft_predicate_NbtPredicate


class NbtPredicateHelper(BaseHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: NbtPredicate) -> None:
		pass

	@overload
	def test(self, entity: EntityHelper) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def test(self, itemStack: ItemStackHelper) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def test(self, nbtElement: NBTElementHelper) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


