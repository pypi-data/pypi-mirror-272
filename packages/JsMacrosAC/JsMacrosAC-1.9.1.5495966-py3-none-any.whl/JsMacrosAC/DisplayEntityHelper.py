from typing import overload
from typing import TypeVar
from typing import Generic
from .EntityHelper import EntityHelper
from .Vec3D import Vec3D

T = TypeVar("T")

class DisplayEntityHelper(Generic[T], EntityHelper):
	"""
	Since: 1.9.1 
	"""

	@overload
	def __init__(self, base: T) -> None:
		pass

	@overload
	def getLerpTargetX(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLerpTargetY(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLerpTargetZ(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLerpTargetPitch(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLerpTargetYaw(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getVisibilityBoundingBox(self) -> Vec3D:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getBillboardMode(self) -> str:
		"""
		Since: 1.9.1 

		Returns:
			"fixed", "vertical", "horizontal" or "center" 
		"""
		pass

	@overload
	def getBrightness(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getSkyBrightness(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getBlockBrightness(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getViewRange(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getShadowRadius(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getShadowStrength(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getDisplayWidth(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getGlowColorOverride(self) -> int:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getLerpProgress(self, delta: float) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	@overload
	def getDisplayHeight(self) -> float:
		"""
		Since: 1.9.1 
		"""
		pass

	pass


