from typing import TypeVar

from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .FChat import FChat
from .FPlayer import FPlayer
from .FRequest import FRequest
from .FJavaUtils import FJavaUtils
from .FKeyBind import FKeyBind
from .FHud import FHud
from .FTime import FTime
from .FJsMacros import FJsMacros
from .FFS import FFS
from .FReflection import FReflection
from .FUtils import FUtils
from .FClient import FClient
from .FWorld import FWorld
from .IFWrapper import IFWrapper
from .FGlobalVars import FGlobalVars
from .FPositionCommon import FPositionCommon

File = TypeVar("java.io.File")



Chat = FChat()
Player = FPlayer()
Request = FRequest()
JavaUtils = FJavaUtils()
KeyBind = FKeyBind()
Hud = FHud()
Time = FTime()
JsMacros = FJsMacros()
FS = FFS()
Reflection = FReflection()
Utils = FUtils()
Client = FClient()
World = FWorld()
JavaWrapper = IFWrapper()
GlobalVars = FGlobalVars()
PositionCommon = FPositionCommon()
context = EventContainer()
file = File()
event = BaseEvent()
