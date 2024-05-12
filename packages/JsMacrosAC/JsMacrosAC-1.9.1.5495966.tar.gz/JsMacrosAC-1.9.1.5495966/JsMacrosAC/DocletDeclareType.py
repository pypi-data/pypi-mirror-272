from typing import overload


class DocletDeclareType:

	@overload
	def name(self) -> str:
		pass

	@overload
	def type(self) -> str:
		pass

	pass


