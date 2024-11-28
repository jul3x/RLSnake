from enum import Enum
from .not_so_bright_bot import NotSoBrightBot
from .human import Human
from .aware_bot import AwareBot
from .collision_aware_bot import CollisionAwareBot


class AgentType(str, Enum):
    HUMAN = 'HUMAN'
    NOT_SO_BRIGHT = 'RANDOM'
    AWARE = 'AWARE'
    COLLISION_AWARE = 'COLLISION_AWARE'
