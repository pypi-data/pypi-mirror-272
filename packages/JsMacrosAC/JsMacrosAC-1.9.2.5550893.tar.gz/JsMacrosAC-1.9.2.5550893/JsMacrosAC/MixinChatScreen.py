from typing import overload
from typing import TypeVar

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen


class MixinChatScreen(Screen):

	@overload
	def onSendChatMessage(self, chatText: str, addToHistory: bool, ci: CallbackInfo) -> None:
		pass

	pass


