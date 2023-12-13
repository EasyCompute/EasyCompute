from enum import Enum

from pydantic import BaseModel


class AVMSize(str, Enum):
    STANDARD_D2S_V3 = "Standard_D2s_v3"
    STANDARD_D4S_V3 = "Standard_D4s_v3"
    STANDARD_D8S_V3 = "Standard_D8s_v3"


class AVMConfig(BaseModel):
    resource_group_name: str
    vm_name: str
    admin_username: str
    size: AVMSize

    location: str = "West US"