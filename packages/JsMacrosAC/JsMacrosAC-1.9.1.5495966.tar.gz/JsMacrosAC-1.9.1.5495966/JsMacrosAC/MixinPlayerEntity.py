from typing import overload
from typing import TypeVar

net_minecraft_entity_LivingEntity = TypeVar("net_minecraft_entity_LivingEntity")
LivingEntity = net_minecraft_entity_LivingEntity

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class MixinPlayerEntity(LivingEntity):

	@overload
	def setCustomName(self, name: Text) -> None:
		pass

	pass


