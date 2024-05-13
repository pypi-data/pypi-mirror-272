from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .ICategoryTreeParent import ICategoryTreeParent
from .MultiElementContainer import MultiElementContainer
from .Scrollbar import Scrollbar
from .Button import Button

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_client_font_TextRenderer = TypeVar("net_minecraft_client_font_TextRenderer")
TextRenderer = net_minecraft_client_font_TextRenderer


class CategoryTreeContainer(ICategoryTreeParent, MultiElementContainer):
	category: str
	scroll: Scrollbar
	children: Mapping[str, "CategoryTreeContainer"]
	expandBtn: Button
	showBtn: Button
	isHead: bool
	topScroll: int
	btnHeight: int

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: ICategoryTreeParent) -> None:
		pass

	@overload
	def addCategory(self, category: List[str]) -> "CategoryTreeContainer":
		pass

	@overload
	def selectCategory(self, category: List[str]) -> None:
		pass

	@overload
	def updateOffsets(self) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def onScrollbar(self, page: float) -> None:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


