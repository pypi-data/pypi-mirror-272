from typing import overload
from typing import TypeVar

R = TypeVar("R")

class Registrable:
	"""
	Since: 1.9.1 
	"""

	@overload
	def register(self) -> R:
		pass

	@overload
	def unregister(self) -> R:
		pass

	pass


