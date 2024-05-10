from __future__ import annotations

__all__ = (
    "BackgroundFill",
    "BackgroundFillSolid",
    "BackgroundFillGradient",
    "BackgroundFillFreeformGradient",
)

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from .abc import TelegramType


@final
class BackgroundFillSolid(TelegramType, tag="solid"):
    """The background is filled using the selected color.

    See: https://core.telegram.org/bots/api#backgroundfillsolid
    """

    color: int
    """The color of the background fill in the RGB24 format."""

    type: ClassVar[Literal["solid"]] = "solid"
    """Type of the background fill, always *solid*"""


@final
class BackgroundFillGradient(TelegramType, tag="gradient"):
    """The background is a gradient fill.

    See: https://core.telegram.org/bots/api#backgroundfillgradient
    """

    top_color: int
    """Top color of the gradient in the RGB24 format."""

    bottom_color: int
    """Bottom color of the gradient in the RGB24 format."""

    rotation_angle: int
    """Clockwise rotation angle of the background fill in degrees; 0-359."""

    type: ClassVar[Literal["gradient"]] = "gradient"
    """Type of the background fill, always *gradient*."""


@final
class BackgroundFillFreeformGradient(TelegramType, tag="freeform_gradient"):
    """The background is a freeform gradient that rotates after every message
    in the chat.

    See: https://core.telegram.org/bots/api#backgroundfillfreeformgradient
    """

    colors: list[int]
    """A list of the 3 or 4 base colors that are used to generate the freeform
    gradient in the RGB24 format.
    """

    type: ClassVar[Literal["freeform_gradient"]] = "freeform_gradient"
    """Type of the background fill, always *freeform_gradient*."""


BackgroundFill: TypeAlias = (
    BackgroundFillSolid
    | BackgroundFillGradient
    | BackgroundFillFreeformGradient
)
"""This object describes the way a background is filled based on the selected
colors.

See: https://core.telegram.org/bots/api#backgroundfill
"""
