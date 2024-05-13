from typing import overload
from typing import TypeVar
from .ClickableWidgetHelper import ClickableWidgetHelper

net_minecraft_client_gui_widget_CheckboxWidget = TypeVar("net_minecraft_client_gui_widget_CheckboxWidget")
CheckboxWidget = net_minecraft_client_gui_widget_CheckboxWidget


class CheckBoxWidgetHelper(ClickableWidgetHelper):
	"""
	Since: 1.8.4 
	"""

	@overload
	def __init__(self, btn: CheckboxWidget) -> None:
		pass

	@overload
	def __init__(self, btn: CheckboxWidget, zIndex: int) -> None:
		pass

	@overload
	def isChecked(self) -> bool:
		"""
		Since: 1.8.4 

		Returns:
			'true' if this button is checked, 'false' otherwise. 
		"""
		pass

	@overload
	def toggle(self) -> "CheckBoxWidgetHelper":
		"""
		Since: 1.8.4 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def setChecked(self, checked: bool) -> "CheckBoxWidgetHelper":
		"""
		Since: 1.8.4 

		Args:
			checked: whether to check or uncheck this button 

		Returns:
			self for chaining. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


