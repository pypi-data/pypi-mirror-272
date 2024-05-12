from typing import overload
from .EventFilterer import EventFilterer
from .BaseEvent import BaseEvent


class FiltererModulus(EventFilterer):
	"""
	Since: 1.9.1 
	"""
	quotient: int
	count: int

	@overload
	def __init__(self, quotient: int) -> None:
		pass

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, event: BaseEvent) -> bool:
		pass

	@overload
	def setQuotient(self, quotient: int) -> "FiltererModulus":
		pass

	pass


