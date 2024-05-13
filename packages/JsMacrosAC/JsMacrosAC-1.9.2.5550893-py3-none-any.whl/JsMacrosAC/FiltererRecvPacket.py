from typing import overload
from .EventFilterer import EventFilterer
from .BaseEvent import BaseEvent


class FiltererRecvPacket(EventFilterer):
	"""
	Since: 1.9.1 
	"""
	type: str

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def canFilter(self, event: str) -> bool:
		pass

	@overload
	def test(self, event: BaseEvent) -> bool:
		pass

	@overload
	def setType(self, type: str) -> "FiltererRecvPacket":
		pass

	pass


