from typing import overload
from typing import List
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper

net_minecraft_scoreboard_ScoreboardObjective = TypeVar("net_minecraft_scoreboard_ScoreboardObjective")
ScoreboardObjective = net_minecraft_scoreboard_ScoreboardObjective


class ScoreboardObjectiveHelper(BaseHelper):
	"""
	Since: 1.2.9 
	"""

	@overload
	def __init__(self, o: ScoreboardObjective) -> None:
		pass

	@overload
	def getPlayerScores(self) -> Mapping[str, int]:
		"""

		Returns:
			player name to score map 
		"""
		pass

	@overload
	def scoreToDisplayName(self) -> Mapping[int, TextHelper]:
		"""
		Since: 1.8.0 
		"""
		pass

	@overload
	def getKnownPlayers(self) -> List[str]:
		"""
		Since: 1.7.0 
		"""
		pass

	@overload
	def getKnownPlayersDisplayNames(self) -> List[TextHelper]:
		"""
		Since: 1.8.0 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""
		Since: 1.2.9 

		Returns:
			name of scoreboard 
		"""
		pass

	@overload
	def getDisplayName(self) -> TextHelper:
		"""
		Since: 1.2.9 

		Returns:
			name of scoreboard 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


