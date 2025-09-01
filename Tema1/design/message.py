import enum, abc
from dataclasses import dataclass


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class MessageParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


class ParserFactory:
    def __init__(self):
        self.__parsers = {}

    def register_parser(self, message_type: MessageType):
        def decorator(parser_cls):
            self.__parsers[message_type] = parser_cls
            return parser_cls
        return decorator

    def get(self, message_type) -> MessageParser:
        return self.__parsers[message_type]


parser_factory = ParserFactory()


@parser_factory.register_parser(MessageType.TELEGRAM)
class TelegramParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


@parser_factory.register_parser(MessageType.MATTERMOST)
class MattermostParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


@parser_factory.register_parser(MessageType.SLACK)
class SlackParser(MessageParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass
