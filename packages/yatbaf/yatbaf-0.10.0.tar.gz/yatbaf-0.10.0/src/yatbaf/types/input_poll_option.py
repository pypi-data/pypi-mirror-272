from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode

    from .message_entity import MessageEntity


@final
class InputPollOption(TelegramType):
    """This object contains information about one answer option in a poll to send.

    See: https://core.telegram.org/bots/api#inputpolloption
    """  # noqa: E501

    text: str
    """Option text, 1-100 characters."""

    text_parse_mode: ParseMode | None = None
    """*Optional.* Mode for parsing entities in the ``text``.  Currently, only
    custom emoji entities are allowed.
    """

    text_entities: list[MessageEntity] | None = None
    """*Optional.* A list of special entities that appear in the poll option
    text. It can be specified instead of ``text_parse_mode``.
    """
