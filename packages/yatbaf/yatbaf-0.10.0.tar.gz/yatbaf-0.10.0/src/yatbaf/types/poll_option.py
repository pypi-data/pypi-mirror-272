from __future__ import annotations

from typing import final

from .abc import TelegramType
from .message_entity import MessageEntity


@final
class PollOption(TelegramType):
    """This object contains information about one answer option in a poll.

    See: https://core.telegram.org/bots/api#polloption
    """

    text: str
    """Option text, 1-100 characters."""

    voter_count: int
    """Number of users that voted for this option."""

    text_entities: list[MessageEntity] | None = None
    """*Optional.* Special entities that appear in the option ``text``.
    Currently, only custom emoji entities are allowed in poll option texts.
    """
