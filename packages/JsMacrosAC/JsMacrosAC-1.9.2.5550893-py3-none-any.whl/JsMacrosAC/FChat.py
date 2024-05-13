from typing import overload
from typing import List
from typing import TypeVar
from .BaseLibrary import BaseLibrary
from .TextHelper import TextHelper
from .TextBuilder import TextBuilder
from .CommandBuilder import CommandBuilder
from .CommandNodeHelper import CommandNodeHelper
from .CommandManager import CommandManager
from .ChatHistoryManager import ChatHistoryManager

org_slf4j_Logger = TypeVar("org_slf4j_Logger")
Logger = org_slf4j_Logger


class FChat(BaseLibrary):
	"""Functions for interacting with chat. 
An instance of this class is passed to scripts as the 'Chat' variable.
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def log(self, message: object) -> None:
		"""Log to player chat.\n
		Since: 1.1.3 

		Args:
			message: 
		"""
		pass

	@overload
	def log(self, message: object, await_: bool) -> None:
		"""

		Args:
			await: should wait for message to actually be sent to chat to continue. 
			message: 
		"""
		pass

	@overload
	def logf(self, message: str, args: List[object]) -> None:
		"""Logs the formatted message to the player's chat. The message is formatted using the default
java String#format(java.lang.String,java.lang.Object...) syntax.\n
		Since: 1.8.4 

		Args:
			args: the arguments used to format the message 
			message: the message to format and log 
		"""
		pass

	@overload
	def logf(self, message: str, await_: bool, args: List[object]) -> None:
		"""Logs the formatted message to the player's chat. The message is formatted using the default
java String#format(java.lang.String,java.lang.Object...) syntax.\n
		Since: 1.8.4 

		Args:
			args: the arguments used to format the message 
			await: whether to wait for message to be sent to chat before continuing 
			message: the message to format and log 
		"""
		pass

	@overload
	def logColor(self, message: str) -> None:
		"""log with auto wrapping with FChat#ampersandToSectionSymbol(java.lang.String)\n
		Since: 1.9.0 

		Args:
			message: 
		"""
		pass

	@overload
	def logColor(self, message: str, await_: bool) -> None:
		"""log with auto wrapping with FChat#ampersandToSectionSymbol(java.lang.String)\n
		Since: 1.9.0 

		Args:
			await: 
			message: 
		"""
		pass

	@overload
	def say(self, message: str) -> None:
		"""Say to server as player.\n
		Since: 1.0.0 

		Args:
			message: 
		"""
		pass

	@overload
	def say(self, message: str, await_: bool) -> None:
		"""Say to server as player.\n
		Since: 1.3.1 

		Args:
			await: 
			message: 
		"""
		pass

	@overload
	def sayf(self, message: str, args: List[object]) -> None:
		"""Sends the formatted message to the server. The message is formatted using the default java String#format(java.lang.String,java.lang.Object...) syntax.\n
		Since: 1.8.4 

		Args:
			args: the arguments used to format the message 
			message: the message to format and send to the server 
		"""
		pass

	@overload
	def sayf(self, message: str, await_: bool, args: List[object]) -> None:
		"""Sends the formatted message to the server. The message is formatted using the default java String#format(java.lang.String,java.lang.Object...) syntax.\n
		Since: 1.8.4 

		Args:
			args: the arguments used to format the message 
			await: whether to wait for message to be sent to chat before continuing 
			message: the message to format and send to the server 
		"""
		pass

	@overload
	def open(self, message: str) -> None:
		"""open the chat input box with specific text already typed.\n
		Since: 1.6.4 

		Args:
			message: the message to start the chat screen with 
		"""
		pass

	@overload
	def open(self, message: str, await_: bool) -> None:
		"""open the chat input box with specific text already typed.
hint: you can combine with FJsMacros#waitForEvent(java.lang.String) or FJsMacros#once(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) to wait for the chat screen
to close and/or the to wait for the sent message\n
		Since: 1.6.4 

		Args:
			await: 
			message: the message to start the chat screen with 
		"""
		pass

	@overload
	def title(self, title: object, subtitle: object, fadeIn: int, remain: int, fadeOut: int) -> None:
		"""Display a Title to the player.\n
		Since: 1.2.1 

		Args:
			fadeOut: 
			fadeIn: 
			remain: 
			subtitle: 
			title: 
		"""
		pass

	@overload
	def actionbar(self, text: object) -> None:
		"""
		Since: 1.8.1 

		Args:
			text: 
		"""
		pass

	@overload
	def actionbar(self, text: object, tinted: bool) -> None:
		"""Display the smaller title that's above the actionbar.\n
		Since: 1.2.1 

		Args:
			tinted: 
			text: 
		"""
		pass

	@overload
	def toast(self, title: object, desc: object) -> None:
		"""Display a toast.\n
		Since: 1.2.5 

		Args:
			title: 
			desc: 
		"""
		pass

	@overload
	def createTextHelperFromString(self, content: str) -> TextHelper:
		"""Creates a TextHelper for use where you need one and not a string.\n
		Since: 1.1.3 

		Args:
			content: 

		Returns:
			a new TextHelper 
		"""
		pass

	@overload
	def createTextHelperFromTranslationKey(self, key: str, content: List[object]) -> TextHelper:
		"""
		Since: 1.9.0 

		Returns:
			a new TextHelper 
		"""
		pass

	@overload
	def getLogger(self) -> Logger:
		"""
		Since: 1.5.2 
		"""
		pass

	@overload
	def getLogger(self, name: str) -> Logger:
		"""returns a log4j logger, for logging to console only.\n
		Since: 1.5.2 

		Args:
			name: 
		"""
		pass

	@overload
	def createTextHelperFromJSON(self, json: str) -> TextHelper:
		"""Create a TextHelper for use where you need one and not a string.\n
		Since: 1.1.3 

		Args:
			json: 

		Returns:
			a new TextHelper 
		"""
		pass

	@overload
	def createTextBuilder(self) -> TextBuilder:
		"""
		Since: 1.3.0 

		Returns:
			a new builder 
		"""
		pass

	@overload
	def createCommandBuilder(self, name: str) -> CommandBuilder:
		"""
		Since: 1.4.2 

		Args:
			name: name of command 
		"""
		pass

	@overload
	def unregisterCommand(self, name: str) -> CommandNodeHelper:
		"""
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def reRegisterCommand(self, node: CommandNodeHelper) -> None:
		"""
		Since: 1.6.5 

		Args:
			node: 
		"""
		pass

	@overload
	def getCommandManager(self) -> CommandManager:
		"""
		Since: 1.7.0 
		"""
		pass

	@overload
	def getHistory(self) -> ChatHistoryManager:
		"""
		Since: 1.7.0 
		"""
		pass

	@overload
	def getTextWidth(self, text: str) -> int:
		"""
		Since: 1.8.4 

		Args:
			text: the text to get the width of 

		Returns:
			the width of the given text in pixels. 
		"""
		pass

	@overload
	def sectionSymbolToAmpersand(self, string: str) -> str:
		"""escapes to since 1.9.0\n
		Since: 1.6.5 

		Args:
			string: 

		Returns:
			-> 
		"""
		pass

	@overload
	def ampersandToSectionSymbol(self, string: str) -> str:
		"""escapes to since 1.9.0\n
		Since: 1.6.5 

		Args:
			string: 

		Returns:
			-> 
		"""
		pass

	@overload
	def stripFormatting(self, string: str) -> str:
		"""
		Since: 1.6.5 

		Args:
			string: 
		"""
		pass

	pass


