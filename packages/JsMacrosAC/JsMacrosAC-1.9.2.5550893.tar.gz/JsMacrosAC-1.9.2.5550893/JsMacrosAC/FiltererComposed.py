from typing import overload
from .EventFilterer_Compound import EventFilterer_Compound
from .EventFilterer import EventFilterer
from .BaseEvent import BaseEvent


class FiltererComposed(EventFilterer_Compound):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, initial: EventFilterer) -> None:
		pass

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, event: BaseEvent) -> bool:
		pass

	@overload
	def and_(self, filterer: EventFilterer) -> "FiltererComposed":
		"""

		Args:
			filterer: the filterer to compose 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def or_(self, filterer: EventFilterer) -> "FiltererComposed":
		"""

		Args:
			filterer: the filterer to compose 

		Returns:
			self for chaining 
		"""
		pass

	@overload
	def checkCyclicRef(self, base: EventFilterer_Compound) -> None:
		pass

	pass


