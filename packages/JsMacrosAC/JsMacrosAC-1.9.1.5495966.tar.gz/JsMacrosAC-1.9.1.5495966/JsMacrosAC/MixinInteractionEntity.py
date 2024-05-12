from typing import overload
from typing import TypeVar
from .IMixinInteractionEntity import IMixinInteractionEntity

org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_ = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_")
CallbackInfoReturnable = org_spongepowered_asm_mixin_injection_callback_CallbackInfoReturnable_java_lang_Boolean_


class MixinInteractionEntity(IMixinInteractionEntity):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_setCanHitOverride(self, value: bool) -> None:
		pass

	@overload
	def overrideCanHit(self, cir: CallbackInfoReturnable) -> None:
		pass

	pass


