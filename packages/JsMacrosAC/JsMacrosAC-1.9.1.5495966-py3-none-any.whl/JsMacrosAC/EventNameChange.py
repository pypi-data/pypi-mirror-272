from typing import overload
from typing import TypeVar
from .BaseEvent import BaseEvent
from .EntityHelper import EntityHelper
from .TextHelper import TextHelper

net_minecraft_entity_Entity = TypeVar("net_minecraft_entity_Entity")
Entity = net_minecraft_entity_Entity

net_minecraft_text_Text = TypeVar("net_minecraft_text_Text")
Text = net_minecraft_text_Text


class EventNameChange(BaseEvent):
	"""
	Since: 1.9.1 
	"""
	entity: EntityHelper
	oldName: TextHelper
	newName: TextHelper

	@overload
	def __init__(self, entity: Entity, oldName: Text, newName: Text) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


