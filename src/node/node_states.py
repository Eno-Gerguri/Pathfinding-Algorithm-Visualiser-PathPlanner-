from enum import IntEnum, auto


class NodeStates(IntEnum):
    ISEMPTY = auto()
    ISBLOCKED = auto()
    ISOPEN = auto()
    ISBARRIER = auto()
    ISSTART = auto()
    ISTARGET = auto()
    ISPATH = auto()
