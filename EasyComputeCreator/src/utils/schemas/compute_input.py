from enum import Enum
from typing import TypedDict, Union
from EasyComputeCreator.src.utils.schemas.aws.auth import AWSAccessKey
from EasyComputeCreator.src.utils.schemas.aws.ec2 import EC2Config
from EasyComputeCreator.src.utils.schemas.azure.auth import AzureAccessKey
from EasyComputeCreator.src.utils.schemas.azure.avm import AVMConfig
from EasyComputeCreator.src.utils.schemas.gcp.auth import GCPAccessKey
from EasyComputeCreator.src.utils.schemas.gcp.gce import GCEConfig


class ComputeType(str, Enum):
    ec2 = "ec2"
    avm = "avm"
    gce = "gce"


class ComputeSchema(TypedDict):
    compute_name: str
    compute_type: ComputeType
    compute_config: Union[EC2Config, AVMConfig, GCEConfig]
    auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey]
