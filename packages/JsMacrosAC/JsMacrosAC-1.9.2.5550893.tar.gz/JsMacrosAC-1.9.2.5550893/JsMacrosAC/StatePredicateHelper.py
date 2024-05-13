from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper
from .BlockStateHelper import BlockStateHelper
from .FluidStateHelper import FluidStateHelper

net_minecraft_predicate_StatePredicate = TypeVar("net_minecraft_predicate_StatePredicate")
StatePredicate = net_minecraft_predicate_StatePredicate


class StatePredicateHelper(BaseHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: StatePredicate) -> None:
		pass

	@overload
	def test(self, state: BlockStateHelper) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def test(self, state: FluidStateHelper) -> bool:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


