from __future__ import annotations

__all__ = (
    "BackgroundType",
    "BackgroundTypeFill",
    "BackgroundTypeWallpaper",
    "BackgroundTypePattern",
    "BackgroundTypeChatTheme",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from yatbaf.typing import NoneBool

from .abc import TelegramType
from .background_fill import BackgroundFill
from .document import Document


@final
class BackgroundTypeFill(TelegramType, tag="fill"):
    """The background is automatically filled based on the selected colors.

    See: https://core.telegram.org/bots/api#backgroundtypefill
    """

    fill: BackgroundFill
    """The background fill."""

    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100."""

    type: ClassVar[Literal["fill"]] = "fill"
    """Type of the background, always *fill*."""


@final
class BackgroundTypeWallpaper(TelegramType, tag="wallpaper"):
    """The background is a wallpaper in the JPEG format.

    See: https://core.telegram.org/bots/api#backgroundtypewallpaper
    """

    document: Document
    """Document with the wallpaper."""

    dark_theme_dimming: int
    """Dimming of the background in dark themes, as a percentage; 0-100."""

    is_blurred: NoneBool = None
    """*Optional.* ``True``, if the wallpaper is downscaled to fit in a 450x450
    square and then box-blurred with radius 12.
    """

    is_moving: NoneBool = None
    """*Optional.* ``True``, if the background moves slightly when the device
    is tilted.
    """

    type: ClassVar[Literal["wallpaper"]] = "wallpaper"
    """Type of the background, always *wallpaper*."""


@final
class BackgroundTypePattern(TelegramType, tag="pattern"):
    """The background is a PNG or TGV (gzipped subset of SVG with MIME type
    "application/x-tgwallpattern") pattern to be combined with the background
    fill chosen by the user.

    See: https://core.telegram.org/bots/api#backgroundtypepattern
    """

    document: Document
    """Document with the pattern."""

    fill: BackgroundFill
    """The background fill that is combined with the pattern."""

    intensity: int
    """Intensity of the pattern when it is shown above the filled background;
    0-100
    """

    is_inverted: NoneBool = None
    """*Optional.* ``True``, if the background fill must be applied only to
    the pattern itself. All other pixels are black in this case. For dark themes
    only.
    """

    is_moving: NoneBool = None
    """*Optional.* ``True``, if the background moves slightly when the device
    is tilted.
    """

    type: ClassVar[Literal["pattern"]] = "pattern"
    """Type of the background, always *pattern*."""


@final
class BackgroundTypeChatTheme(TelegramType, tag="chat_theme"):
    """The background is taken directly from a built-in chat theme.

    See: https://core.telegram.org/bots/api#backgroundtypechattheme
    """

    theme_name: str
    """Name of the chat theme, which is usually an emoji."""

    type: ClassVar[Literal["chat_theme"]] = "chat_theme"
    """Type of the background, always *chat_theme*."""


BackgroundType: TypeAlias = (
    BackgroundTypeFill
    | BackgroundTypeWallpaper
    | BackgroundTypePattern
    | BackgroundTypeChatTheme
)
"""This object describes the type of a background.

See: https://core.telegram.org/bots/api#backgroundtype
"""
