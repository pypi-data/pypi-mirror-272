from strenum import LowercaseStrEnum
from typing import Literal, Union


class PostType(LowercaseStrEnum):
    TEXT = "text"
    PHOTO = "photo"
    QUOTE = "quote"
    LINK = "link"
    CHAT = "chat"
    AUDIO = "audio"
    VIDEO = "video"


PostTypeTyping = Union[Literal["text", "photo", "quote", "link", "chat", "audio", "video"], PostType]


class PostFilter(LowercaseStrEnum):
    HTML = "html"
    TEXT = "text"
    RAW = "raw"


PostFilterTyping = Union[Literal["html", "text", "raw"], PostFilter]


class PostState(LowercaseStrEnum):
    PUBLISHED = "published"
    DRAFT = "draft"
    QUEUE = "queue"
    PRIVATE = "private"


PostStateTyping = Union[Literal['published', 'draft', 'queue', 'private'], PostState]


class PostFormat(LowercaseStrEnum):
    HTML = "html"
    MARKDOWN = "markdown"


PostFormatTyping = Union[Literal['html', 'markdown'], PostFormat]
