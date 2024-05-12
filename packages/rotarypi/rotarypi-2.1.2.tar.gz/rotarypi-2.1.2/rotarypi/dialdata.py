import json
from typing import Union
from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    """
    Enumeration to discriminate specific types of events:
    - DIAL_EVENT is emitted when a number is dialed on the rotary dial
    - HANDSET_EVENT is emitted when the handset is picked up or hung up
    """
    DIAL_EVENT = 0
    HANDSET_EVENT = 1


class HandsetState(Enum):
    """
    Enumeration to discriminate what kind of HANDSET_EVENT is emitted
    """
    HUNG_UP = 0
    PICKED_UP = 1


@dataclass(frozen=True)
class DialEvent:
    """
    Data class to emit whenever something happens with the phone.
    For every event, an instance of this class is put into the queue.
    """
    type: EventType
    data: Union[HandsetState, int]

    def __repr__(self):
        j = {"type": self.type.value}
        if isinstance(self.data, int):
            j["data"] = self.data
        else:
            j["data"] = self.data.value
        return json.dumps(j)

    def __str__(self):
        return f"DIAL EVENT\n\ttype: {self.type}\n\tdata: {self.data}"
