from typing import overload
from typing import TypeVar
from typing import Generic
from .LivingEntityHelper import LivingEntityHelper
from .PlayerAbilitiesHelper import PlayerAbilitiesHelper
from .ItemStackHelper import ItemStackHelper
from .FishingBobberEntityHelper import FishingBobberEntityHelper

T = TypeVar("T")

class PlayerEntityHelper(Generic[T], LivingEntityHelper):
	"""
	"""

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getPlayerName(self) -> str:
		"""get player's actual name. (not display name)\n
		Since: 1.8.4 
		"""
		pass

	@overload
	def getAbilities(self) -> PlayerAbilitiesHelper:
		"""
		Since: 1.0.3 
		"""
		pass

	@overload
	def getMainHand(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getOffHand(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getHeadArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getChestArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getLegArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getFootArmor(self) -> ItemStackHelper:
		"""
		Since: 1.2.0 
		"""
		pass

	@overload
	def getXP(self) -> int:
		"""
		Since: 1.2.5 [citation needed] 
		"""
		pass

	@overload
	def getXPLevel(self) -> int:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getXPProgress(self) -> float:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getXPToLevelUp(self) -> int:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def isSleeping(self) -> bool:
		"""
		Since: 1.2.5 [citation needed] 
		"""
		pass

	@overload
	def isSleepingLongEnough(self) -> bool:
		"""
		Since: 1.2.5 [citation needed] 

		Returns:
			if the player has slept the minimum amount of time to pass the night. 
		"""
		pass

	@overload
	def getFishingBobber(self) -> FishingBobberEntityHelper:
		"""
		Since: 1.8.4 

		Returns:
			the fishing bobber of the player, or 'null' if the player is not fishing. 
		"""
		pass

	@overload
	def getAttackCooldownProgress(self) -> float:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getAttackCooldownProgressPerTick(self) -> float:
		"""
		Since: 1.8.4 
		"""
		pass

	@overload
	def getScore(self) -> int:
		"""
		Since: 1.8.4 

		Returns:
			the player's score. 
		"""
		pass

	pass


