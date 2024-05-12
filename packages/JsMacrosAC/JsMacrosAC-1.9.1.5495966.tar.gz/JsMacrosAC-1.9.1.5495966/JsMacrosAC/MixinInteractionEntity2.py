from typing import overload


class MixinInteractionEntity2:

	@overload
	def callGetInteractionWidth(self) -> float:
		pass

	@overload
	def callGetInteractionHeight(self) -> float:
		pass

	@overload
	def callShouldRespond(self) -> bool:
		pass

	pass


