from typing import overload
from typing import TypeVar

org_joml_Matrix4f = TypeVar("org_joml_Matrix4f")
Matrix4f = org_joml_Matrix4f

org_spongepowered_asm_mixin_injection_callback_CallbackInfo = TypeVar("org_spongepowered_asm_mixin_injection_callback_CallbackInfo")
CallbackInfo = org_spongepowered_asm_mixin_injection_callback_CallbackInfo

net_minecraft_client_render_GameRenderer = TypeVar("net_minecraft_client_render_GameRenderer")
GameRenderer = net_minecraft_client_render_GameRenderer

net_minecraft_client_render_Camera = TypeVar("net_minecraft_client_render_Camera")
Camera = net_minecraft_client_render_Camera

net_minecraft_client_render_LightmapTextureManager = TypeVar("net_minecraft_client_render_LightmapTextureManager")
LightmapTextureManager = net_minecraft_client_render_LightmapTextureManager


class MixinWorldRenderer:

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def renderInvisibleOutline(self, tickDelta: float, limitTime: float, renderBlockOutline: bool, camera: Camera, gameRenderer: GameRenderer, lightmapTextureManager: LightmapTextureManager, matrix4f: Matrix4f, matrix4f2: Matrix4f, ci: CallbackInfo) -> None:
		pass

	pass


