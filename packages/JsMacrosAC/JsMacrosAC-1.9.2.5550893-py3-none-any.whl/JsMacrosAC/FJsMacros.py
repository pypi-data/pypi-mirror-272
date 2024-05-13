from typing import overload
from typing import List
from .PerExecLibrary import PerExecLibrary
from .BaseScriptContext import BaseScriptContext
from .BaseProfile import BaseProfile
from .ConfigManager import ConfigManager
from .ServiceManager import ServiceManager
from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .MethodWrapper import MethodWrapper
from .IEventListener import IEventListener
from .EventFilterer import EventFilterer
from .FJsMacros_EventAndContext import FJsMacros_EventAndContext
from .FiltererComposed import FiltererComposed
from .FiltererModulus import FiltererModulus
from .EventCustom import EventCustom


class FJsMacros(PerExecLibrary):
	"""Functions that interact directly with JsMacros or Events. 
An instance of this class is passed to scripts as the 'JsMacros' variable.
	"""

	@overload
	def __init__(self, context: BaseScriptContext) -> None:
		pass

	@overload
	def getProfile(self) -> BaseProfile:
		"""

		Returns:
			the JsMacros profile class. 
		"""
		pass

	@overload
	def getConfig(self) -> ConfigManager:
		"""

		Returns:
			the JsMacros config management class. 
		"""
		pass

	@overload
	def getServiceManager(self) -> ServiceManager:
		"""services are background scripts designed to run full time and are mainly noticed by their side effects.\n
		Since: 1.6.3 

		Returns:
			for managing services. 
		"""
		pass

	@overload
	def getOpenContexts(self) -> List[BaseScriptContext]:
		"""
		Since: 1.4.0 

		Returns:
			list of non-garbage-collected ScriptContext's 
		"""
		pass

	@overload
	def runScript(self, file: str) -> EventContainer:
		"""
		Since: 1.1.5 

		Args:
			file: 
		"""
		pass

	@overload
	def runScript(self, file: str, fakeEvent: BaseEvent) -> EventContainer:
		"""
		Since: 1.6.3 

		Args:
			file: 
			fakeEvent: you probably actually want to pass an instance created by FJsMacros#createCustomEvent(java.lang.String) 
		"""
		pass

	@overload
	def runScript(self, file: str, fakeEvent: BaseEvent, callback: MethodWrapper) -> EventContainer:
		"""runs a script with a eventCustom to be able to pass args\n
		Since: 1.6.3 (1.1.5 - 1.6.3 didn't have fakeEvent) 

		Args:
			file: 
			fakeEvent: 
			callback: 

		Returns:
			container the script is running on. 
		"""
		pass

	@overload
	def runScript(self, language: str, script: str) -> EventContainer:
		"""
		Since: 1.2.4 

		Args:
			language: 
			script: 
		"""
		pass

	@overload
	def runScript(self, language: str, script: str, callback: MethodWrapper) -> EventContainer:
		"""Runs a string as a script.\n
		Since: 1.2.4 

		Args:
			callback: calls your method as a Consumer String 
			language: 
			script: 

		Returns:
			the EventContainer the script is running on. 
		"""
		pass

	@overload
	def runScript(self, language: str, script: str, file: str, callback: MethodWrapper) -> EventContainer:
		"""
		Since: 1.6.0 

		Args:
			file: 
			callback: 
			language: 
			script: 
		"""
		pass

	@overload
	def runScript(self, language: str, script: str, file: str, event: BaseEvent, callback: MethodWrapper) -> EventContainer:
		"""
		Since: 1.7.0 

		Args:
			file: 
			callback: 
			language: 
			event: 
			script: 
		"""
		pass

	@overload
	def wrapScriptRun(self, file: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			file: 
			T: 
			U: 
		"""
		pass

	@overload
	def wrapScriptRun(self, language: str, script: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			T: 
			U: 
			language: 
			script: 
		"""
		pass

	@overload
	def wrapScriptRun(self, language: str, script: str, file: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			file: 
			T: 
			U: 
			language: 
			script: 
		"""
		pass

	@overload
	def wrapScriptRunAsync(self, file: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			file: 
			T: 
			U: 
		"""
		pass

	@overload
	def wrapScriptRunAsync(self, language: str, script: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			T: 
			U: 
			language: 
			script: 
		"""
		pass

	@overload
	def wrapScriptRunAsync(self, language: str, script: str, file: str) -> MethodWrapper:
		"""
		Since: 1.7.0 

		Args:
			R: 
			file: 
			T: 
			U: 
			language: 
			script: 
		"""
		pass

	@overload
	def open(self, path: str) -> None:
		"""Opens a file with the default system program.\n
		Since: 1.1.8 

		Args:
			path: relative to the script's folder. 
		"""
		pass

	@overload
	def openUrl(self, url: str) -> None:
		"""
		Since: 1.6.0 

		Args:
			url: 
		"""
		pass

	@overload
	def on(self, event: str, callback: MethodWrapper) -> IEventListener:
		"""Creates a listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.2.7 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 
		"""
		pass

	@overload
	def on(self, event: str, joined: bool, callback: MethodWrapper) -> IEventListener:
		"""Creates a listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.9.0 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 
		"""
		pass

	@overload
	def on(self, event: str, filterer: EventFilterer, callback: MethodWrapper) -> IEventListener:
		"""Creates a listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.9.1 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 
		"""
		pass

	@overload
	def on(self, event: str, filterer: EventFilterer, joined: bool, callback: MethodWrapper) -> IEventListener:
		"""Creates a listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.9.1 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 
		"""
		pass

	@overload
	def once(self, event: str, callback: MethodWrapper) -> IEventListener:
		"""Creates a single-run listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.2.7 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 

		Returns:
			the listener. 
		"""
		pass

	@overload
	def once(self, event: str, joined: bool, callback: MethodWrapper) -> IEventListener:
		"""Creates a single-run listener for an event, this function can be more efficient that running a script file when used properly.\n
		Since: 1.9.0 

		Args:
			callback: calls your method as a BiConsumer BaseEvent , EventContainer 
			event: 

		Returns:
			the listener. 
		"""
		pass

	@overload
	def off(self, listener: IEventListener) -> bool:
		"""
		Since: 1.2.3 

		Args:
			listener: 
		"""
		pass

	@overload
	def off(self, event: str, listener: IEventListener) -> bool:
		"""Removes a IEventListener from an event.\n
		Since: 1.2.3 

		Args:
			listener: 
			event: 
		"""
		pass

	@overload
	def disableAllListeners(self, event: str) -> None:
		"""Will also disable all listeners for the given event, including JsMacros own event listeners.\n
		Since: 1.8.4 

		Args:
			event: the event to remove all listeners from 
		"""
		pass

	@overload
	def disableAllListeners(self) -> None:
		"""Will also disable all listeners, including JsMacros own event listeners.\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def disableScriptListeners(self, event: str) -> None:
		"""Will only disable user created event listeners for the given event. This includes listeners
created from FJsMacros#on(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) , FJsMacros#once(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) , FJsMacros#waitForEvent(java.lang.String) , FJsMacros#waitForEvent(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,java.lang.Object,java.lang.Boolean,?>) and FJsMacros#waitForEvent(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,java.lang.Object,java.lang.Boolean,?>,xyz.wagyourtail.jsmacros.core.MethodWrapper<java.lang.Object,java.lang.Object,java.lang.Object,?>) .\n
		Since: 1.8.4 

		Args:
			event: the event to remove all listeners from 
		"""
		pass

	@overload
	def disableScriptListeners(self) -> None:
		"""Will only disable user created event listeners.  This includes listeners created from FJsMacros#on(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) , FJsMacros#once(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,xyz.wagyourtail.jsmacros.core.language.EventContainer<?>,java.lang.Object,?>) , FJsMacros#waitForEvent(java.lang.String) , FJsMacros#waitForEvent(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,java.lang.Object,java.lang.Boolean,?>) and FJsMacros#waitForEvent(java.lang.String,xyz.wagyourtail.jsmacros.core.MethodWrapper<xyz.wagyourtail.jsmacros.core.event.BaseEvent,java.lang.Object,java.lang.Boolean,?>,xyz.wagyourtail.jsmacros.core.MethodWrapper<java.lang.Object,java.lang.Object,java.lang.Object,?>) .\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def waitForEvent(self, event: str) -> FJsMacros_EventAndContext:
		"""
		Since: 1.5.0 

		Args:
			event: event to wait for 

		Returns:
			a event and a new context if the event you're waiting for was joined, to leave it early. 
		"""
		pass

	@overload
	def waitForEvent(self, event: str, join: bool) -> FJsMacros_EventAndContext:
		"""
		Since: 1.9.0 

		Args:
			event: event to wait for 

		Returns:
			a event and a new context if the event you're waiting for was joined, to leave it early. 
		"""
		pass

	@overload
	def waitForEvent(self, event: str, filter: MethodWrapper) -> FJsMacros_EventAndContext:
		"""
		Since: 1.5.0 [citation needed] 

		Args:
			event: 
		"""
		pass

	@overload
	def waitForEvent(self, event: str, join: bool, filter: MethodWrapper) -> FJsMacros_EventAndContext:
		"""
		Since: 1.9.0 

		Args:
			event: 
		"""
		pass

	@overload
	def waitForEvent(self, event: str, filter: MethodWrapper, runBeforeWaiting: MethodWrapper) -> FJsMacros_EventAndContext:
		"""waits for an event. if this thread is bound to an event already, this will release current lock.\n
		Since: 1.5.0 

		Args:
			filter: filter the event until it has the proper values or whatever. 
			runBeforeWaiting: runs as a Runnable , run before waiting, this is a thread-safety thing to prevent "interrupts" from going in between this and things like deferCurrentTask 
			event: event to wait for 

		Returns:
			a event and a new context if the event you're waiting for was joined, to leave it early. 
		"""
		pass

	@overload
	def waitForEvent(self, event: str, join: bool, filter: MethodWrapper, runBeforeWaiting: MethodWrapper) -> FJsMacros_EventAndContext:
		"""waits for an event. if this thread is bound to an event already, this will release current lock.\n
		Since: 1.9.0 

		Args:
			filter: filter the event until it has the proper values or whatever. 
			runBeforeWaiting: runs as a Runnable , run before waiting, this is a thread-safety thing to prevent "interrupts" from going in between this and things like deferCurrentTask 
			event: event to wait for 

		Returns:
			a event and a new context if the event you're waiting for was joined, to leave it early. 
		"""
		pass

	@overload
	def listeners(self, event: str) -> List[IEventListener]:
		"""
		Since: 1.2.3 

		Args:
			event: 

		Returns:
			a list of script-added listeners. 
		"""
		pass

	@overload
	def createEventFilterer(self, event: str) -> EventFilterer:
		"""create an event filterer. this exists to reduce lag when listening to frequently triggered events.\n
		Since: 1.9.1 
		"""
		pass

	@overload
	def createComposedEventFilterer(self, initial: EventFilterer) -> FiltererComposed:
		"""create a composed event filterer. this filterer combines multiple filterers together with and/or logic.\n
		Since: 1.9.1 
		"""
		pass

	@overload
	def createModulusEventFilterer(self, quotient: int) -> FiltererModulus:
		"""create a modulus event filterer. this filterer only let every nth event pass through.\n
		Since: 1.9.1 
		"""
		pass

	@overload
	def invertEventFilterer(self, base: EventFilterer) -> EventFilterer:
		"""inverts the base filterer's result. this checks if the base is already inverted. e.g. 'filterer == invert(invert(filterer))' would be 'true' .\n
		Since: 1.9.1 
		"""
		pass

	@overload
	def createCustomEvent(self, eventName: str) -> EventCustom:
		"""create a custom event object that can trigger a event. It's recommended to use EventCustom#registerEvent() to set up the event to be visible in the GUI.\n
		Since: 1.2.8 

		Args:
			eventName: name of the event. please don't use an existing one... your scripts might not like that. 
		"""
		pass

	@overload
	def assertEvent(self, event: BaseEvent, type: str) -> None:
		"""asserts if 'event' is the correct type of event and convert 'event' type to target type in ts example: JsMacros.assertEvent(event, 'Service')\n
		Since: 1.9.0 

		Args:
			event: the event to assert 
			type: string of the event type 
		"""
		pass

	pass


