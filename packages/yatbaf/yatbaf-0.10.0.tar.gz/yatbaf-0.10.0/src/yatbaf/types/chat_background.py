from __future__ import annotations

from typing import final

from .abc import TelegramType
from .background_type import BackgroundType


@final
class ChatBackground(TelegramType):
    """This object represents a chat background.

    See: https://core.telegram.org/bots/api#chatbackground
    """

    type: BackgroundType
    """Type of the background."""
