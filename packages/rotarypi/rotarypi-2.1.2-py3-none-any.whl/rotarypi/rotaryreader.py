from queue import Queue
import RPi.GPIO as GPIO
from typing import Optional
from threading import Lock
import logging
import sys
import time

from rotarypi import DialPinout, DialConfiguration, EventType, HandsetState, DialEvent


class RotaryReader:
    """
    Detect state changes of the handset and read the rotary dial
    """

    def __init__(self, queue: Queue[DialEvent], pinout: Optional[DialPinout] = None, config: Optional[DialConfiguration] = None):
        self.queue: Queue[DialEvent] = queue
        self.pinout = pinout if pinout is not None else DialPinout()
        self.config = config if config is not None else DialConfiguration()
        self.logger = self._setup_logging()
        self.gpio = GPIO
        self.gpio.setmode(GPIO.BCM)
        self.rotating = False
        self.counter_lock = Lock()
        self.counter = 0
        self._setup()

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("RotaryLogger")
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.config.loglevel)
        return logger

    def _setup(self):
        self.gpio.setup(self.pinout.dial_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(self.pinout.counter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(self.pinout.handset_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _dialpin_callback(self, channel):
        self.logger.debug("Dial pin callback")
        time.sleep(self.config.dial_bounceback/1000)
        state = self.gpio.input(channel)
        if state:
            self.rotating = False
            self.logger.debug("Rotation finished")
            if self.counter > 0:
                self.counter_lock.acquire()
                val = self.counter % 10
                msg = DialEvent(
                    type=EventType.DIAL_EVENT,
                    data=val
                )
                self.queue.put(msg)
                self.logger.info(f"queued {val}")
            self.counter = 0
            self.counter_lock.release()
        else:
            self.rotating = True
            self.logger.debug("Rotation started")

    def _count_dial_callback(self, channel):
        self.logger.debug("Count pin callback")
        self.counter_lock.acquire()
        self.counter += 1
        self.counter_lock.release()

    def _handset_callback(self, channel):
        self.logger.debug("Handset callback")
        time.sleep(self.config.handset_bounceback/1000)
        state = self.gpio.input(channel)
        if state:
            msg = DialEvent(
                type=EventType.HANDSET_EVENT,
                data=HandsetState.HUNG_UP
            )
            self.logger.info("Handset was hung up")
        else:
            msg = DialEvent(
                type=EventType.HANDSET_EVENT,
                data=HandsetState.PICKED_UP
            )
            self.logger.info("Handset was picked up")
        self.queue.put(msg)

    def start(self):
        """
        Start listening to events by attaching edge detection on
        the GPIO pins. This method is non-blocking.
        """
        self.gpio.add_event_detect(
            self.pinout.dial_pin, self.gpio.BOTH,
            callback=self._dialpin_callback,
            bouncetime=self.config.dial_debounce
        )
        self.gpio.add_event_detect(
            self.pinout.counter_pin, self.gpio.RISING,
            callback=self._count_dial_callback,
            bouncetime=self.config.counter_debounce
        )
        self.gpio.add_event_detect(
            self.pinout.handset_pin, self.gpio.BOTH,
            callback=self._handset_callback,
            bouncetime=self.config.handset_debounce
        )
        self.logger.info("Callbacks attached, started listening")

    def stop(self):
        """
        Stop listening to events by detaching attached edge detection.
        """
        self.gpio.remove_event_detect(self.pinout.dial_pin)
        self.gpio.remove_event_detect(self.pinout.counter_pin)
        self.gpio.remove_event_detect(self.pinout.handset_pin)
        self.logger.info("Callbacks detached, stopped listening")

    def cleanup(self):
        """
        Cleanup the used GPIO pins.
        """
        self.gpio.cleanup()
