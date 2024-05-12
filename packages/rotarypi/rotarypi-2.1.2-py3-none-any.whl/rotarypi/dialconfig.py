import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class DialPinout:
    """
    Define the pin numbers the phone hardware is attached to.
    """
    counter_pin: int = 19
    dial_pin: int = 26
    handset_pin: int = 13


@dataclass(frozen=True)
class DialConfiguration:
    """
    Configuration for the RotaryReader. Mainly defines timings for
    switch debouncing.
    """
    loglevel: int = logging.WARNING
    counter_debounce: int = 80
    dial_debounce: int = 100
    handset_debounce: int = 200
    dial_bounceback: int = 20
    handset_bounceback: int = 20
