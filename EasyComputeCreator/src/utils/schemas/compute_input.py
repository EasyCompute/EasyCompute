from enum import Enum
from typing import TypedDict, Union, List

from pydantic import BaseModel, constr


# Auth Configs
class AWSAccessKey(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str


class GCPAccessKey(BaseModel):
    project_id: str
    credentials: str


class AzureAccessKey(BaseModel):
    subscription_id: str
    client_id: str
    secret: str
    tenant: str


# Compute Types
class ComputeType(str, Enum):
    ec2 = "ec2"
    avm = "avm"
    gce = "gce"


# Compute Kwargs


# Define valid machine types as Enums
class GCEMachineType(str, Enum):
    N1_STANDARD_1 = "n1-standard-1"
    N1_STANDARD_2 = "n1-standard-2"
    N1_STANDARD_4 = "n1-standard-4"


class EC2AMIs(str, Enum):
    AMAZON_LINUX_AMI = "/aws/service/ami-amazon-linux-latest/amzn-ami-hvm-x86_64-gp2"
    AMAZON_LINUX_2_AMI = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
    UBUNTU_16_04_LTS = "/aws/service/ami-ubuntu-latest/ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"
    UBUNTU_18_04_LTS = "/aws/service/ami-ubuntu-latest/ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"
    RHEL_7_5 = "/aws/service/ami-redhat-latest/rhel-7.5-x86_64*"
    WINDOWS_SERVER_CORE_2019 = (
        "/aws/service/ami-windows-latest/Windows_Server-2019-English-Core-Base-*"
    )
    WINDOWS_SERVER_2019 = (
        "/aws/service/ami-windows-latest/Windows_Server-2019-English-Full-Base-*"
    )
    WINDOWS_SERVER_2016 = (
        "/aws/service/ami-windows-latest/Windows_Server-2016-English-Full-Base-*"
    )
    WINDOWS_SERVER_2012_R2 = "/aws/service/ami-windows-latest/Windows_Server-2012-R2_RTM-English-64Bit-Base-*"
    WINDOWS_SERVER_2012 = (
        "/aws/service/ami-windows-latest/Windows_Server-2012-RTM-English-64Bit-Base-*"
    )
    WINDOWS_SERVER_2008_R2_SP1 = "/aws/service/ami-windows-latest/Windows_Server-2008-R2_SP1-English-64Bit-Base-*"
    SUSE_LINUX_ENTERPRISE_SERVER = (
        "/aws/service/ami-suse-latest/suse-sles-15-sp1-v20200129-hvm-ssd-x86_64*"
    )
    FEDORA_SERVER = "/aws/service/ami-fedora-latest/fedora-29-x86_64-*"
    DEBIAN_9 = "/aws/service/ami-debian-latest/debian-9-amd64-*"
    DEBIAN_10 = "/aws/service/ami-debian-latest/debian-10-amd64-*"
    CENTOS_7 = "/aws/service/ami-centos-latest/centos-7-x86_64-*"
    CENTOS_8 = "/aws/service/ami-centos-latest/centos-8-x86_64-*"
    FREEBSD_12 = "/aws/service/ami-freebsd-latest/freebsd-12*-amd64-*"
    DEEP_LEARNING_AMI = "/aws/service/ami-dl-latest-1/amzn2-ami-dl-*"
    ELASTIC_GRAPHICS_AMI = (
        "/aws/service/ami-eg-latest/Windows_Server-2019-English-Full-ECS_Optimized-*"
    )
    ELASTIC_INFERENCE_AMI = (
        "/aws/service/ami-ei-latest/Windows_Server-2019-English-Full-ECS_Optimized-*"
    )
    AWS_PARALLELCLUSTER_AMI = "/aws/service/ami-pcl-latest-*"


class EC2InstanceType(str, Enum):
    T2_MICRO = "t2.micro"
    T2_SMALL = "t2.small"
    T2_MEDIUM = "t2.medium"


class AVMSize(str, Enum):
    STANDARD_D2S_V3 = "Standard_D2s_v3"
    STANDARD_D4S_V3 = "Standard_D4s_v3"
    STANDARD_D8S_V3 = "Standard_D8s_v3"


class EC2Config(BaseModel):
    image_id: EC2AMIs
    instance_type: EC2InstanceType
    key_name: str
    region_name: str = "us-east-1"
    create_key_pair: bool = False
    security_group_ids: list = None

    max_instance_count: int = 1
    min_instance_count: int = 1


class AVMConfig(BaseModel):
    resource_group_name: str
    vm_name: str
    admin_username: str
    size: AVMSize

    location: str = "West US"


class GCEConfig(BaseModel):
    project: str
    zone: str
    name: str
    machine_type: GCEMachineType

    disk_type: str = "pd-standard"
    disk_size: str = "100GB"


# Overall Compute Schema
class ComputeSchema(TypedDict):
    compute_name: str
    compute_type: ComputeType
    compute_config: Union[EC2Config, AVMConfig, GCEConfig]
    auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey]
