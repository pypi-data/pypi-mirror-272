from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class WriteType(Enum):
    NONE = 0
    RAW = 1
    RAW_COMPRESSED = 2


@dataclass
class WriteArgs:
    write_type: WriteType
    fov: str
    series_description: str
    study_description: str
    protocol: str
    date_time: datetime | str
    root_site_id: str = "1.2.826.0.1.3680043.10.1341"
    downsample_factor: int = 0
    height: int = 0
    width: int = 0
    length: int = 0
    is_rgb: bool = False
    is_hdr: bool = False
