from typing import overload
from typing import TypeVar

net_minecraft_registry_entry_RegistryEntry_net_minecraft_entity_effect_StatusEffect_ = TypeVar("net_minecraft_registry_entry_RegistryEntry_net_minecraft_entity_effect_StatusEffect_")
RegistryEntry = net_minecraft_registry_entry_RegistryEntry_net_minecraft_entity_effect_StatusEffect_


class IBeaconScreen:

	@overload
	def jsmacros_getPrimaryEffect(self) -> RegistryEntry:
		pass

	@overload
	def jsmacros_setPrimaryEffect(self, effect: RegistryEntry) -> None:
		pass

	@overload
	def jsmacros_getSecondaryEffect(self) -> RegistryEntry:
		pass

	@overload
	def jsmacros_setSecondaryEffect(self, effect: RegistryEntry) -> None:
		pass

	pass


