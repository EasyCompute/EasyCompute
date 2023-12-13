from dataclasses import dataclass, field
from typing import List, Optional, Union
from enum import Enum
from datetime import datetime


# Enums and simple data structures
class VolumeType(Enum):
    STANDARD = 'standard'
    IO1 = 'io1'
    IO2 = 'io2'
    GP2 = 'gp2'
    SC1 = 'sc1'
    ST1 = 'st1'
    GP3 = 'gp3'


class InstanceType(Enum):
    A1_MEDIUM = 'a1.medium'
    A1_LARGE = 'a1.large'
    A1_XLARGE = 'a1.xlarge'
    A1_2XLARGE = 'a1.2xlarge'
    A1_4XLARGE = 'a1.4xlarge'
    A1_METAL = 'a1.metal'
    C1_MEDIUM = 'c1.medium'
    C1_XLARGE = 'c1.xlarge'
    C3_LARGE = 'c3.large'
    C3_XLARGE = 'c3.xlarge'
    C3_2XLARGE = 'c3.2xlarge'
    C3_4XLARGE = 'c3.4xlarge'
    C3_8XLARGE = 'c3.8xlarge'
    C4_LARGE = 'c4.large'
    C4_XLARGE = 'c4.xlarge'
    C4_2XLARGE = 'c4.2xlarge'
    C4_4XLARGE = 'c4.4xlarge'
    C4_8XLARGE = 'c4.8xlarge'
    C5_LARGE = 'c5.large'
    C5_XLARGE = 'c5.xlarge'
    C5_2XLARGE = 'c5.2xlarge'
    C5_4XLARGE = 'c5.4xlarge'
    C5_9XLARGE = 'c5.9xlarge'
    C5_12XLARGE = 'c5.12xlarge'
    C5_18XLARGE = 'c5.18xlarge'
    C5_24XLARGE = 'c5.24xlarge'


class EC2AMI(str, Enum):
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


# Data classes
@dataclass
class EbsOptions:
    DeleteOnTermination: bool
    Iops: Optional[int] = None
    SnapshotId: Optional[str] = None
    VolumeSize: Optional[int] = None
    VolumeType: Optional[VolumeType] = None
    KmsKeyId: Optional[str] = None
    Throughput: Optional[int] = None
    OutpostArn: Optional[str] = None
    Encrypted: Optional[bool] = None


@dataclass
class BlockDeviceMapping:
    DeviceName: str
    VirtualName: Optional[str] = None
    Ebs: Optional[EbsOptions] = None
    NoDevice: Optional[str] = None


@dataclass
class Monitoring:
    Enabled: bool


@dataclass
class IamInstanceProfile:
    Arn: Optional[str] = None
    Name: Optional[str] = None


@dataclass
class Placement:
    AvailabilityZone: Optional[str] = None
    Affinity: Optional[str] = None
    GroupName: Optional[str] = None
    PartitionNumber: Optional[int] = None
    HostId: Optional[str] = None
    Tenancy: Optional[str] = None
    SpreadDomain: Optional[str] = None
    HostResourceGroupArn: Optional[str] = None
    GroupId: Optional[str] = None


@dataclass
class NetworkInterface:
    AssociatePublicIpAddress: Optional[bool] = None
    DeleteOnTermination: Optional[bool] = None
    Description: Optional[str] = None
    DeviceIndex: Optional[int] = None
    Groups: Optional[List[str]] = None
    Ipv6AddressCount: Optional[int] = None
    Ipv6Addresses: Optional[List[str]] = None
    NetworkInterfaceId: Optional[str] = None
    PrivateIpAddress: Optional[str] = None
    PrivateIpAddresses: Optional[List[str]] = None
    SecondaryPrivateIpAddressCount: Optional[int] = None
    SubnetId: Optional[str] = None
    AssociateCarrierIpAddress: Optional[bool] = None
    InterfaceType: Optional[str] = None
    NetworkCardIndex: Optional[int] = None
    Ipv4Prefixes: Optional[List[str]] = None
    Ipv4PrefixCount: Optional[int] = None
    Ipv6Prefixes: Optional[List[str]] = None
    Ipv6PrefixCount: Optional[int] = None
    PrimaryIpv6: Optional[bool] = None


@dataclass
class ElasticGpuSpecification:
    Type: str


@dataclass
class ElasticInferenceAccelerator:
    Type: str
    Count: int


@dataclass
class Tag:
    Key: str
    Value: str


@dataclass
class TagSpecification:
    ResourceType: str
    Tags: List[Tag]


@dataclass
class LaunchTemplateSpecification:
    LaunchTemplateId: Optional[str] = None
    LaunchTemplateName: Optional[str] = None
    Version: Optional[str] = None


@dataclass
class SpotOptions:
    MaxPrice: Optional[str] = None
    SpotInstanceType: Optional[str] = None
    BlockDurationMinutes: Optional[int] = None
    ValidUntil: Optional[datetime] = None
    InstanceInterruptionBehavior: Optional[str] = None


@dataclass
class InstanceMarketOptions:
    MarketType: Optional[str] = None
    SpotOptions: Optional[SpotOptions] = None


@dataclass
class CreditSpecification:
    CpuCredits: Optional[str] = None


@dataclass
class CpuOptions:
    CoreCount: Optional[int] = None
    ThreadsPerCore: Optional[int] = None
    AmdSevSnp: Optional[str] = None


@dataclass
class CapacityReservationTarget:
    CapacityReservationId: Optional[str] = None
    CapacityReservationResourceGroupArn: Optional[str] = None


@dataclass
class CapacityReservationSpecification:
    CapacityReservationPreference: Optional[str] = None
    CapacityReservationTarget: Optional[CapacityReservationTarget] = None


@dataclass
class HibernationOptions:
    Configured: bool


@dataclass
class LicenseSpecification:
    LicenseConfigurationArn: str


@dataclass
class MetadataOptions:
    HttpTokens: Optional[str] = None
    HttpPutResponseHopLimit: Optional[int] = None
    HttpEndpoint: Optional[str] = None
    HttpProtocolIpv6: Optional[str] = None
    InstanceMetadataTags: Optional[str] = None


@dataclass
class EnclaveOptions:
    Enabled: bool


@dataclass
class PrivateDnsNameOptions:
    HostnameType: str
    EnableResourceNameDnsARecord: bool
    EnableResourceNameDnsAAAARecord: bool


@dataclass
class MaintenanceOptions:
    AutoRecovery: Optional[str] = None


# Main request class
@dataclass
class EC2Config:
    BlockDeviceMappings: List[BlockDeviceMapping]
    ImageId: EC2AMI
    InstanceType: InstanceType
    MaxCount: int
    MinCount: int
    Ipv6AddressCount: Optional[int] = None
    Ipv6Addresses: Optional[List[str]] = None
    KernelId: Optional[str] = None
    KeyName: Optional[str] = None
    Monitoring: Optional[Monitoring] = None
    Placement: Optional[Placement] = None
    RamdiskId: Optional[str] = None
    SecurityGroupIds: Optional[List[str]] = None
    SecurityGroups: Optional[List[str]] = None
    SubnetId: Optional[str] = None
    UserData: Optional[str] = None
    AdditionalInfo: Optional[str] = None
    ClientToken: Optional[str] = None
    DisableApiTermination: Optional[bool] = None
    DryRun: Optional[bool] = None
    EbsOptimized: Optional[bool] = None
    IamInstanceProfile: Optional[IamInstanceProfile] = None
    InstanceInitiatedShutdownBehavior: Optional[str] = None
    NetworkInterfaces: Optional[List[NetworkInterface]] = None
    PrivateIpAddress: Optional[str] = None
    ElasticGpuSpecification: Optional[List[ElasticGpuSpecification]] = None
    ElasticInferenceAccelerators: Optional[List[ElasticInferenceAccelerator]] = None
    TagSpecifications: Optional[List[TagSpecification]] = None
    LaunchTemplate: Optional[LaunchTemplateSpecification] = None
    InstanceMarketOptions: Optional[InstanceMarketOptions] = None
    CreditSpecification: Optional[CreditSpecification] = None
    CpuOptions: Optional[CpuOptions] = None
    CapacityReservationSpecification: Optional[CapacityReservationSpecification] = None
    HibernationOptions: Optional[HibernationOptions] = None
    LicenseSpecifications: Optional[List[LicenseSpecification]] = None
    MetadataOptions: Optional[MetadataOptions] = None
    EnclaveOptions: Optional[EnclaveOptions] = None
    PrivateDnsNameOptions: Optional[PrivateDnsNameOptions] = None
    MaintenanceOptions: Optional[MaintenanceOptions] = None
