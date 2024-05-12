from typing import overload
from typing import TypeVar
from typing import Mapping
from .BaseHelper import BaseHelper
from .TextHelper import TextHelper
from .NBTElementHelper_NBTCompoundHelper import NBTElementHelper_NBTCompoundHelper
from .BlockStateHelper import BlockStateHelper
from .BlockHelper import BlockHelper
from .BlockPosHelper import BlockPosHelper

net_minecraft_block_BlockState = TypeVar("net_minecraft_block_BlockState")
BlockState = net_minecraft_block_BlockState

net_minecraft_block_Block = TypeVar("net_minecraft_block_Block")
Block = net_minecraft_block_Block

net_minecraft_util_math_BlockPos = TypeVar("net_minecraft_util_math_BlockPos")
BlockPos = net_minecraft_util_math_BlockPos

net_minecraft_block_entity_BlockEntity = TypeVar("net_minecraft_block_entity_BlockEntity")
BlockEntity = net_minecraft_block_entity_BlockEntity


class BlockDataHelper(BaseHelper):
	"""
	"""

	@overload
	def __init__(self, b: BlockState, e: BlockEntity, bp: BlockPos) -> None:
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.1.7 

		Returns:
			the 'x' value of the block. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.1.7 

		Returns:
			the 'y' value of the block. 
		"""
		pass

	@overload
	def getZ(self) -> int:
		"""
		Since: 1.1.7 

		Returns:
			the 'z' value of the block. 
		"""
		pass

	@overload
	def getId(self) -> str:
		"""

		Returns:
			the item ID of the block. 
		"""
		pass

	@overload
	def getName(self) -> TextHelper:
		"""

		Returns:
			the translated name of the block. (was string before 1.6.5) 
		"""
		pass

	@overload
	def getNBT(self) -> NBTElementHelper_NBTCompoundHelper:
		"""
		Since: 1.5.1, used to be a Map String , String 
		"""
		pass

	@overload
	def getBlockStateHelper(self) -> BlockStateHelper:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getBlockHelper(self) -> BlockHelper:
		"""
		Since: 1.6.5 
		"""
		pass

	@overload
	def getBlock(self) -> BlockHelper:
		"""
		Since: 1.6.5 

		Returns:
			the block 
		"""
		pass

	@overload
	def getBlockState(self) -> Mapping[str, str]:
		"""
		Since: 1.1.7 

		Returns:
			block state data as a Map . 
		"""
		pass

	@overload
	def getBlockPos(self) -> BlockPosHelper:
		"""
		Since: 1.2.7 

		Returns:
			the block pos. 
		"""
		pass

	@overload
	def getRawBlock(self) -> Block:
		pass

	@overload
	def getRawBlockState(self) -> BlockState:
		pass

	@overload
	def getRawBlockEntity(self) -> BlockEntity:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


