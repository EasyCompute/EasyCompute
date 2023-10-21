import logging
import os
from abc import abstractproperty, abstractmethod
from typing import Union

import boto3
from azure.mgmt.compute import ComputeManagementClient
from envyaml import EnvYAML

from src.utils.schemas.compute_input import (
    EC2Config,
    AWSAccessKey, ComputeType, ComputeSchema, AVMConfig, GCEConfig, GCPAccessKey, AzureAccessKey,
)

logger = logging.getLogger(__name__)


class Client:
    def __init__(
            self,
            compute_name: str,
            compute_type: ComputeType,
            compute_config: Union[EC2Config, AVMConfig, GCEConfig],
            auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey],
    ):
        self.compute_name: str = compute_name
        self.compute_type: ComputeType = compute_type
        self._compute_config: Union[EC2Config, AVMConfig, GCEConfig] = compute_config
        self._auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey] = auth_config

        self.client: Union[
            boto3.client, compute.ComputeClient, ComputeManagementClient
        ]

    @abstractmethod
    def compute_name(self):
        pass

    @abstractmethod
    def client(self):
        pass

    @abstractmethod
    def build_compute_instance(self):
        pass
