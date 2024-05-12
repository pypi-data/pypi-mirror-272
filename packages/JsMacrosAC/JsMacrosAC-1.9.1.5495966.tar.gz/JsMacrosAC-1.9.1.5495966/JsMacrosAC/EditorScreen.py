from typing import overload
from typing import List
from typing import TypeVar
from .BaseScreen import BaseScreen
from .History import History
from .SelectCursor import SelectCursor
from .AbstractRenderCodeCompiler import AbstractRenderCodeCompiler

net_minecraft_client_gui_screen_Screen = TypeVar("net_minecraft_client_gui_screen_Screen")
Screen = net_minecraft_client_gui_screen_Screen

net_minecraft_client_gui_DrawContext = TypeVar("net_minecraft_client_gui_DrawContext")
DrawContext = net_minecraft_client_gui_DrawContext

net_minecraft_text_Style = TypeVar("net_minecraft_text_Style")
Style = net_minecraft_text_Style

java_io_File = TypeVar("java_io_File")
File = java_io_File


class EditorScreen(BaseScreen):
	langs: List[str]
	defaultStyle: Style
	history: History
	cursor: SelectCursor
	blockFirst: bool
	textRenderTime: float
	prevChar: str
	language: str
	codeCompiler: AbstractRenderCodeCompiler

	@overload
	def __init__(self, parent: Screen, file: File) -> None:
		pass

	@overload
	def getDefaultLanguage(self) -> str:
		pass

	@overload
	def openAndScrollToIndex(self, file: File, startIndex: int, endIndex: int) -> None:
		pass

	@overload
	def openAndScrollToLine(self, file: File, line: int, col: int, endCol: int) -> None:
		pass

	@overload
	def setScroll(self, pages: float) -> None:
		pass

	@overload
	def setLanguage(self, language: str) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def copyToClipboard(self) -> None:
		pass

	@overload
	def pasteFromClipboard(self) -> None:
		pass

	@overload
	def cutToClipboard(self) -> None:
		pass

	@overload
	def keyPressed(self, keyCode: int, scanCode: int, modifiers: int) -> bool:
		pass

	@overload
	def scrollToCursor(self) -> None:
		pass

	@overload
	def save(self) -> None:
		pass

	@overload
	def needSave(self) -> bool:
		pass

	@overload
	def mouseScrolled(self, mouseX: float, mouseY: float, horiz: float, vert: float) -> bool:
		pass

	@overload
	def render(self, drawContext: DrawContext, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def openParent(self) -> None:
		pass

	@overload
	def mouseClicked(self, mouseX: float, mouseY: float, btn: int) -> bool:
		pass

	@overload
	def selectWordAtCursor(self) -> None:
		pass

	@overload
	def mouseDragged(self, mouseX: float, mouseY: float, button: int, deltaX: float, deltaY: float) -> bool:
		pass

	@overload
	def updateSettings(self) -> None:
		pass

	@overload
	def charTyped(self, chr: str, keyCode: int) -> bool:
		pass

	pass


