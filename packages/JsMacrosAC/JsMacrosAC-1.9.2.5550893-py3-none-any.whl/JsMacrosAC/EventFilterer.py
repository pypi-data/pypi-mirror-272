from typing import overload
from .BaseEvent import BaseEvent


class EventFilterer:
	"""
	Since: 1.9.1 
	"""

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, event: BaseEvent) -> bool:
		pass

	pass


