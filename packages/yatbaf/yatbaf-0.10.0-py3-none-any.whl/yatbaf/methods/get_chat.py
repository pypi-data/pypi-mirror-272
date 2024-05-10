from __future__ import annotations

from typing import final

from yatbaf.types import ChatFullInfo

from .abc import TelegramMethod


@final
class GetChat(TelegramMethod[ChatFullInfo]):
    """See :meth:`yatbaf.bot.Bot.get_chat`"""

    chat_id: str | int
