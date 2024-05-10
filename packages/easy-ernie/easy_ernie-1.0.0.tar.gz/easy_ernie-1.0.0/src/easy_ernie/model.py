import enum
import dataclasses

class BotModel(enum.Enum):
    EB3_5 = 'EB35'
    EB4_0 = 'EB40'

@dataclasses.dataclass
class SessionBase:
    sessionId: str
    name: str
    botModel: str
    creationTimestamp: int

@dataclasses.dataclass
class Session:
    tops: list[SessionBase]
    normals: list[SessionBase]

@dataclasses.dataclass
class SessionDetailBase:
    name: str
    botModel: str
    creationTimestamp: int

@dataclasses.dataclass
class SessionDetailHistory:
    chatId: str
    role: str
    text: str
    creationTimestamp: int

@dataclasses.dataclass
class SessionDetail:
    base: SessionDetailBase
    histories: list[SessionDetailHistory]
    currentChatId: str

@dataclasses.dataclass
class Response:
    answer: str
    urls: list
    sessionId: str
    botChatId: str

@dataclasses.dataclass
class AskStreamResponse(Response):
    done: bool

@dataclasses.dataclass
class AskResponse(Response):
    pass