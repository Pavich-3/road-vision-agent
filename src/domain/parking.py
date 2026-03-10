from dataclasses import dataclass
from .gps import Gps


@dataclass
class Parking:
    empty_count: int
    gps: Gps