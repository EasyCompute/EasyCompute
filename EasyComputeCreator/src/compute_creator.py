import logging
import os
from abc import abstractproperty, abstractmethod
from typing import Union

import boto3
from azure.mgmt.compute import ComputeManagementClient
from envyaml import EnvYAML

from EasyComputeCreator.src.utils.schemas.compute_input import (
    EC2Config,
    AWSAccessKey, ComputeType, ComputeSchema, AVMConfig, GCEConfig, GCPAccessKey, AzureAccessKey,
)
from EasyComputeCreator.src.utils.service.aws import AWSClient
from EasyComputeCreator.src.utils.service.azure import AzureClient
from EasyComputeCreator.src.utils.service.gcp import GCPClient

logger = logging.getLogger(__name__)

TYPE_MAP = {
    "ec2": AWSClient,
    "gce": GCPClient,
    "avm": AzureClient,
}


class ComputeCreator:
    def __init__(
            self,
            compute_config_location: str = os.environ.get(
                "COMPUTE_CONFIG_LOCATION", "config/compute_config.yaml"
            ),
    ):
        compute_schema = compute_name, compute_type, compute_config, auth_config = self.validate_inputs(
            compute_config_location
        )
        self.compute_name: str = compute_name
        self.compute_type: ComputeType = compute_type
        self._compute_config: Union[EC2Config, AVMConfig, GCEConfig] = compute_config
        self._auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey] = auth_config

        self.client: Union[
            boto3.client, compute.ComputeClient, ComputeManagementClient
        ] = TYPE_MAP[self.compute_type](*compute_schema)

    @property
    def compute_name(self):
        return self._compute_name

    @compute_name.setter
    def compute_name(self, compute_name: str):
        self._compute_name = compute_name

    def build_compute_instance(self):
        self.client.build_compute_instance()

    @staticmethod
    def validate_inputs(compute_config_location: str):
        """
        Validate inputs for compute creation.
        """
        yaml_data = EnvYAML(compute_config_location).export()
        try:
            compute_schema = ComputeSchema(**yaml_data)
            logger.info("Validation successful!")
            return (
                compute_schema["compute_name"],
                compute_schema["compute_type"],
                compute_schema["compute_config"],
                compute_schema["auth_config"],
            )
        except Exception as e:
            logger.error(f"Validation failed. Error: {str(e)}")
