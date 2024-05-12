from typing import overload
from .EventFilterer import EventFilterer


class EventFilterer_Compound(EventFilterer):

	@overload
	def checkCyclicRef(self, base: "EventFilterer_Compound") -> None:
		pass

	pass


