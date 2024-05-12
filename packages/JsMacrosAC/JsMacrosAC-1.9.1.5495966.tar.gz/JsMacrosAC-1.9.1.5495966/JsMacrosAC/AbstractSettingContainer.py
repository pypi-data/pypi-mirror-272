from typing import overload
from typing import List
from typing import TypeVar
from .MultiElementContainer import MultiElementContainer
from .Scrollbar import Scrollbar
from .SettingsOverlay import SettingsOverlay
from .SettingsOverlay_SettingField import SettingsOverlay_SettingField

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class AbstractSettingContainer(MultiElementContainer):
	group: List[str]
	scroll: Scrollbar

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addSetting(self, setting: SettingsOverlay_SettingField) -> None:
		pass

	pass


