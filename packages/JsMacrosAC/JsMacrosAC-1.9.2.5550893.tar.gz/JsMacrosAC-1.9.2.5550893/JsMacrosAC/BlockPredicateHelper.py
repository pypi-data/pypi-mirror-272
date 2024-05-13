from typing import overload
from typing import List
from typing import TypeVar
from .BaseHelper import BaseHelper
from .BlockHelper import BlockHelper
from .StatePredicateHelper import StatePredicateHelper
from .NbtPredicateHelper import NbtPredicateHelper
from .BlockPosHelper import BlockPosHelper

net_minecraft_predicate_BlockPredicate = TypeVar("net_minecraft_predicate_BlockPredicate")
BlockPredicate = net_minecraft_predicate_BlockPredicate


class BlockPredicateHelper(BaseHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: BlockPredicate) -> None:
		pass

	@overload
	def getBlocks(self) -> List[BlockHelper]:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getStatePredicate(self) -> StatePredicateHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getNbtPredicate(self) -> NbtPredicateHelper:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def test(self, state: BlockPosHelper) -> bool:
		"""
		Since: 1.9.1 

		Args:
			state: 
		"""
		pass

	pass


