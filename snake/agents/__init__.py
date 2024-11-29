from enum import Enum
from .not_so_bright_bot import NotSoBrightBot
from .human import Human
from .aware_bot import AwareBot
from .collision_aware_bot import CollisionAwareBot
from .rl_agent import RLAgent


class AgentType(str, Enum):
    HUMAN = 'HUMAN'
    NOT_SO_BRIGHT = 'RANDOM'
    AWARE = 'AWARE'
    COLLISION_AWARE = 'COLLISION_AWARE'
    RL_TRAIN = 'RL_TRAIN'

    def get_agent_type(self):
        match self:
            case AgentType.HUMAN:
                return Human
            case AgentType.NOT_SO_BRIGHT:
                return NotSoBrightBot
            case AgentType.AWARE:
                return AwareBot
            case AgentType.COLLISION_AWARE:
                return CollisionAwareBot
            case AgentType.RL_TRAIN:
                return RLAgent
