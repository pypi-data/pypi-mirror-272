from typing import overload
from typing import TypeVar
from typing import Mapping
from typing import Set
from typing import Generic
from .BaseEvent import BaseEvent
from .EventContainer import EventContainer
from .BaseScriptContext_SleepRunnable import BaseScriptContext_SleepRunnable

T = TypeVar("T")
java_lang_ref_WeakReference_java_lang_Object_ = TypeVar("java_lang_ref_WeakReference_java_lang_Object_")
WeakReference = java_lang_ref_WeakReference_java_lang_Object_

java_io_File = TypeVar("java_io_File")
File = java_io_File

java_util_WeakHashMap_xyz_wagyourtail_jsmacros_core_event_IEventListener,java_lang_String_ = TypeVar("java_util_WeakHashMap_xyz_wagyourtail_jsmacros_core_event_IEventListener,java_lang_String_")
WeakHashMap = java_util_WeakHashMap_xyz_wagyourtail_jsmacros_core_event_IEventListener,java_lang_String_

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class BaseScriptContext(Generic[T]):
	"""
	Since: 1.4.0 
	"""
	startTime: float
	syncObject: WeakReference
	triggeringEvent: BaseEvent
	eventListeners: WeakHashMap
	hasMethodWrapperBeenInvoked: bool

	@overload
	def __init__(self, event: BaseEvent, file: File) -> None:
		pass

	@overload
	def getSyncObject(self) -> object:
		"""this object should only be weak referenced unless we want to prevent the context from closing when syncObject is cleared.
		"""
		pass

	@overload
	def clearSyncObject(self) -> None:
		pass

	@overload
	def shouldKeepAlive(self) -> bool:
		pass

	@overload
	def getBoundEvents(self) -> Mapping[Thread, EventContainer]:
		"""
		Since: 1.6.0 
		"""
		pass

	@overload
	def bindEvent(self, th: Thread, event: EventContainer) -> None:
		"""
		Since: 1.6.0 

		Args:
			th: 
			event: 
		"""
		pass

	@overload
	def releaseBoundEventIfPresent(self, thread: Thread) -> bool:
		"""
		Since: 1.6.0 

		Args:
			thread: 
		"""
		pass

	@overload
	def getContext(self) -> T:
		pass

	@overload
	def getMainThread(self) -> Thread:
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def bindThread(self, t: Thread) -> bool:
		"""
		Since: 1.6.0 

		Args:
			t: 

		Returns:
			is a newly bound thread 
		"""
		pass

	@overload
	def unbindThread(self, t: Thread) -> None:
		"""
		Since: 1.6.0 

		Args:
			t: 
		"""
		pass

	@overload
	def getBoundThreads(self) -> Set[Thread]:
		"""
		Since: 1.6.0 
		"""
		pass

	@overload
	def setMainThread(self, t: Thread) -> None:
		"""
		Since: 1.5.0 

		Args:
			t: 
		"""
		pass

	@overload
	def getTriggeringEvent(self) -> BaseEvent:
		"""
		Since: 1.5.0 
		"""
		pass

	@overload
	def setContext(self, context: T) -> None:
		pass

	@overload
	def isContextClosed(self) -> bool:
		pass

	@overload
	def closeContext(self) -> None:
		pass

	@overload
	def getFile(self) -> File:
		"""
		Since: 1.6.0 
		"""
		pass

	@overload
	def getContainedFolder(self) -> File:
		"""
		Since: 1.6.0 
		"""
		pass

	@overload
	def isMultiThreaded(self) -> bool:
		pass

	@overload
	def wrapSleep(self, sleep: BaseScriptContext_SleepRunnable) -> None:
		pass

	pass


