from typing import overload


class IMixinInteractionEntity:

	@overload
	def jsmacros_setCanHitOverride(self, value: bool) -> None:
		pass

	pass


