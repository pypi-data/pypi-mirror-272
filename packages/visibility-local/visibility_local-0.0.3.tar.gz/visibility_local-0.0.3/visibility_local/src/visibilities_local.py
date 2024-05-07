from enum import Enum

class VisibilitiesLocal (Enum):
    NO_ONE = 0
    ONLY_CREATOR = 1
    # TODO Can we use Python MAX VALUE const
    EVERYONE = 18446744073709551615