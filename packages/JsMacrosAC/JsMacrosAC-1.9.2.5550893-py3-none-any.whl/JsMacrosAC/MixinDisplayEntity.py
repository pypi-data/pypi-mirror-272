from typing import overload
from typing import TypeVar

net_minecraft_entity_decoration_Brightness = TypeVar("net_minecraft_entity_decoration_Brightness")
Brightness = net_minecraft_entity_decoration_Brightness

net_minecraft_entity_decoration_DisplayEntity_BillboardMode = TypeVar("net_minecraft_entity_decoration_DisplayEntity_BillboardMode")
DisplayEntity_BillboardMode = net_minecraft_entity_decoration_DisplayEntity_BillboardMode


class MixinDisplayEntity:

	@overload
	def callGetBrightnessUnpacked(self) -> Brightness:
		pass

	@overload
	def callGetViewRange(self) -> float:
		pass

	@overload
	def callGetShadowRadius(self) -> float:
		pass

	@overload
	def callGetShadowStrength(self) -> float:
		pass

	@overload
	def callGetDisplayWidth(self) -> float:
		pass

	@overload
	def callGetGlowColorOverride(self) -> int:
		pass

	@overload
	def callGetDisplayHeight(self) -> float:
		pass

	@overload
	def callGetBillboardMode(self) -> DisplayEntity_BillboardMode:
		pass

	pass


