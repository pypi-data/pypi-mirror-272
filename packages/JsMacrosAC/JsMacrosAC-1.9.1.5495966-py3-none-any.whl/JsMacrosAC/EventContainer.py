from typing import overload
from typing import TypeVar
from typing import Generic

T = TypeVar("T")
java_lang_Runnable = TypeVar("java_lang_Runnable")
Runnable = java_lang_Runnable

java_lang_Thread = TypeVar("java_lang_Thread")
Thread = java_lang_Thread


class EventContainer(Generic[T]):
	"""
	Since: 1.4.0 
	"""

	@overload
	def __init__(self, ctx: T) -> None:
		pass

	@overload
	def isLocked(self) -> bool:
		pass

	@overload
	def setLockThread(self, lockThread: Thread) -> None:
		pass

	@overload
	def getCtx(self) -> T:
		pass

	@overload
	def getLockThread(self) -> Thread:
		pass

	@overload
	def awaitLock(self, then: Runnable) -> None:
		"""careful with this one it can cause deadlocks if used in scripts incorrectly.\n
		Since: 1.4.0 

		Args:
			then: must be a MethodWrapper when called from a script. 
		"""
		pass

	@overload
	def releaseLock(self) -> None:
		"""can be released earlier in a script or language impl.\n
		Since: 1.4.0 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


