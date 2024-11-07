"""Moves the input text left to right and back in a continuous cycle.

Classes:
    HorizontalCycle: Moves the input text left to right and back.
    HorizontalCycleConfig: Configuration for the HorizontalCycle effect.
    HorizontalCycleIterator: Iterator for the HorizontalCycle effect.
"""

from __future__ import annotations

import typing
from dataclasses import dataclass

import terminaltexteffects.utils.argvalidators as argvalidators
from terminaltexteffects.utils.graphics import Color, Gradient
from terminaltexteffects.engine.base_effect import BaseEffect, BaseEffectIterator
from terminaltexteffects.utils.argsdataclass import ArgField, ArgsDataClass, argclass
from terminaltexteffects.utils.easing import in_cubic


def get_effect_and_args() -> tuple[type[typing.Any], type[ArgsDataClass]]:
    return HorizontalCycle, HorizontalCycleConfig


@argclass(
    name="horizontalcycle",
    help="Moves the input text left to right and back in a continuous cycle.",
    description="horizontalcycle | Moves the input text left to right and back in a continuous cycle.",
    epilog="Example: terminaltexteffects horizontalcycle --speed 0.1 --amplitude 5",
)
@dataclass
class HorizontalCycleConfig(ArgsDataClass):
    """Configuration for the HorizontalCycle effect.

    Attributes:
        speed (float): Speed of the animation as the delay between frames in seconds.
        amplitude (int): Maximum displacement of the text from its original position.
    """

    speed: float = ArgField(
        cmd_name=["--speed"],
        type_parser=argvalidators.PositiveFloat.type_parser,
        default=0.1,
        metavar=argvalidators.PositiveFloat.METAVAR,
        help="Speed of the animation as the delay between frames in seconds.",
    )  # type: ignore[assignment]

    "float : Speed of the animation as the delay between frames in seconds."

    amplitude: int = ArgField(
        cmd_name=["--amplitude"],
        type_parser=argvalidators.PositiveInt.type_parser,
        default=5,
        metavar=argvalidators.PositiveInt.METAVAR,
        help="Maximum displacement of the text from its original position.",
    )  # type: ignore[assignment]

    "int : Maximum displacement of the text from its original position."

    @classmethod
    def get_effect_class(cls):
        return HorizontalCycle


class HorizontalCycleIterator(BaseEffectIterator[HorizontalCycleConfig]):
    def __init__(self, effect: "HorizontalCycle") -> None:
        super().__init__(effect)
        self.amplitude = self.config.amplitude
        self.speed = self.config.speed
        self.current_offset = 0
        self.direction = 1
        self.build()

    def build(self) -> None:
        for character in self.terminal.get_characters():
            self.terminal.set_character_visibility(character, True)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        self.update()

        for character in self.terminal.get_characters():
            if not character.is_active:
                gradient_scn = character.animation.new_scene(ease=in_cubic)
                gradient = Gradient(
                    Color("ffffff"),
                    Color("ff0000"),
                    Color("ffffff"),
                    steps=10,
                )
                gradient_scn.apply_gradient_to_symbols(
                    gradient,
                    character.input_symbol,
                    5,
                )
                character.animation.activate_scene(gradient_scn)
                self.active_characters.append(character)

        return self.frame


class HorizontalCycle(BaseEffect[HorizontalCycleConfig]):
    """Moves the input text left to right and back in a continuous cycle.

    Attributes:
        effect_config (HorizontalCycleConfig): Configuration for the effect.
        terminal_config (TerminalConfig): Configuration for the terminal.
    """

    _config_cls = HorizontalCycleConfig
    _iterator_cls = HorizontalCycleIterator

    def __init__(self, input_data: str) -> None:
        """Initialize the effect with the provided input data.

        Args:
            input_data (str): The input data to use for the effect."""
        super().__init__(input_data)
