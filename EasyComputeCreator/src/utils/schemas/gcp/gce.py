from enum import Enum

from pydantic import BaseModel


class GCEMachineType(str, Enum):
    N1_STANDARD_1 = "n1-standard-1"
    N1_STANDARD_2 = "n1-standard-2"
    N1_STANDARD_4 = "n1-standard-4"


class GCEConfig(BaseModel):
    project: str
    zone: str
    name: str
    machine_type: GCEMachineType

    disk_type: str = "pd-standard"
    disk_size: str = "100GB"
