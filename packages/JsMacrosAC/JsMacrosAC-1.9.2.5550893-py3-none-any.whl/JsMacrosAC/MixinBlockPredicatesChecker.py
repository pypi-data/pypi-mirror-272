from typing import overload
from typing import List
from typing import TypeVar

net_minecraft_predicate_BlockPredicate = TypeVar("net_minecraft_predicate_BlockPredicate")
BlockPredicate = net_minecraft_predicate_BlockPredicate


class MixinBlockPredicatesChecker:

	@overload
	def getPredicates(self) -> List[BlockPredicate]:
		pass

	pass


