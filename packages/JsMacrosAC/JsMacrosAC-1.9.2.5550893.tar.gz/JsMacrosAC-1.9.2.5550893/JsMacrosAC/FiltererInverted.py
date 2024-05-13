from typing import overload
from .EventFilterer_Compound import EventFilterer_Compound
from .EventFilterer import EventFilterer
from .BaseEvent import BaseEvent


class FiltererInverted(EventFilterer_Compound):
	"""
	Since: 1.9.1 
	"""
	base: EventFilterer

	@overload
	def invert(self, base: EventFilterer) -> EventFilterer:
		pass

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, event: BaseEvent) -> bool:
		pass

	@overload
	def checkCyclicRef(self, base: EventFilterer_Compound) -> None:
		pass

	pass


