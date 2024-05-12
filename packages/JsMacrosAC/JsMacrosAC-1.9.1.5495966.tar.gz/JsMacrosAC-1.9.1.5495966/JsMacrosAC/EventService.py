from typing import overload
from typing import List
from typing import Mapping
from .BaseEvent import BaseEvent
from .MethodWrapper import MethodWrapper
from .Registrable import Registrable


class EventService(BaseEvent):
	"""
	Since: 1.6.4 
	"""
	serviceName: str
	stopListener: MethodWrapper
	postStopListener: MethodWrapper

	@overload
	def __init__(self, name: str) -> None:
		pass

	@overload
	def unregisterOnStop(self, offEvents: bool, list: List[Registrable]) -> None:
		"""Setup unregister on stop. For example, 'event.unregisterOnStop(false, d2d);' is
the equivalent of 'event.stopListener = JavaWrapper.methodToJava(() => d2d.unregister());' .  If this is called multiple times, the previous ones would be discarded.  The order of execution is run stopListener -> off events -> unregister stuff -> run postStopListener.  If anything was set to unregister, the service won't stop by itself even if it reaches the end.\n
		Since: 1.9.1 

		Args:
			offEvents: whether the service manager should clear event listeners that the callback doesn't belong to this context. 
			list: the list of registrable, such as Draw2D, Draw3D and CommandBuilder. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def putInt(self, name: str, i: int) -> int:
		"""Put an Integer into the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
			i: 
		"""
		pass

	@overload
	def putString(self, name: str, str: str) -> str:
		"""put a String into the global variable space.\n
		Since: 1.6.5 

		Args:
			str: 
			name: 
		"""
		pass

	@overload
	def putDouble(self, name: str, d: float) -> float:
		"""put a Double into the global variable space.\n
		Since: 1.6.5 

		Args:
			d: 
			name: 
		"""
		pass

	@overload
	def putBoolean(self, name: str, b: bool) -> bool:
		"""put a Boolean into the global variable space.\n
		Since: 1.6.5 

		Args:
			b: 
			name: 
		"""
		pass

	@overload
	def putObject(self, name: str, o: object) -> object:
		"""put anything else into the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
			o: 
		"""
		pass

	@overload
	def getType(self, name: str) -> str:
		"""Returns the type of the defined item in the global variable space as a string.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getInt(self, name: str) -> int:
		"""Gets an Integer from the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getAndIncrementInt(self, name: str) -> int:
		"""Gets an Integer from the global variable space. and then increment it there.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getAndDecrementInt(self, name: str) -> int:
		"""Gets an integer from the global variable pace. and then decrement it there.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def incrementAndGetInt(self, name: str) -> int:
		"""increment an Integer in the global variable space. then return it.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def decrementAndGetInt(self, name: str) -> int:
		"""decrement an Integer in the global variable space. then return it.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getString(self, name: str) -> str:
		"""Gets a String from the global variable space\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getDouble(self, name: str) -> float:
		"""Gets a Double from the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getBoolean(self, name: str) -> bool:
		"""Gets a Boolean from the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def toggleBoolean(self, name: str) -> bool:
		"""toggles a global boolean and returns its new value\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def getObject(self, name: str) -> object:
		"""Gets an Object from the global variable space.\n
		Since: 1.6.5 

		Args:
			name: 
		"""
		pass

	@overload
	def remove(self, key: str) -> None:
		"""removes a key from the global variable space.\n
		Since: 1.6.5 

		Args:
			key: 
		"""
		pass

	@overload
	def getRaw(self) -> Mapping[str, object]:
		pass

	pass


