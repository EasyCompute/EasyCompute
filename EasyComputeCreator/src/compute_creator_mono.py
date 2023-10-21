import logging
import os
from typing import Union

import boto3
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from envyaml import EnvYAML
from google.cloud import compute
from google.oauth2 import service_account

from src.utils.schemas.compute_input import (
    ComputeSchema,
    EC2Config,
    GCEConfig,
    AVMConfig,
    ComputeType, AWSAccessKey, GCPAccessKey, AzureAccessKey,
)

logger = logging.getLogger(__name__)


class ComputeCreator:
    def __init__(
        self,
        compute_config_location: str = os.environ.get(
            "COMPUTE_CONFIG_LOCATION", "config/compute_config.yaml"
        ),
    ):
        """
        Compute Creator class to create compute instances.

        Args:
            compute_config_location: location of the compute config file
        """
        compute_name, compute_type, compute_config, auth_config = self._validate_inputs(
            compute_config_location
        )
        self.compute_name: str = compute_name
        self.compute_type: ComputeType = compute_type
        self.compute_config: Union[EC2Config, AVMConfig, GCEConfig] = compute_config
        self._auth_config: Union[AWSAccessKey, GCPAccessKey, AzureAccessKey] = auth_config
        self._client: Union[
            boto3.client, compute.ComputeClient, ComputeManagementClient
        ] = self._generate_client()

    @property
    def compute_name(self):
        return self._compute_name

    @compute_name.setter
    def compute_name(self, compute_name: str):
        self._compute_name = compute_name

    @property
    def compute_type(self):
        return self._compute_type

    @compute_type.setter
    def compute_type(self, compute_type: str):
        self._compute_type = compute_type

    @property
    def compute_config(self):
        return self._compute_config

    @compute_config.setter
    def compute_config(self, compute_config: dict):
        self._compute_config = compute_config

    def build(self):
        """
        Build the compute instance.
        """
        instance_builder = {
            "ec2": self._build_ec2_instance,
            "avm": self._build_avm_instance,
            "gce": self._build_gce_instance,
        }

        if self.compute_type in instance_builder:
            instance_builder[self.compute_type](self._compute_config)
        else:
            raise ValueError(f"Invalid instance_type: {self.compute_type}")

    @staticmethod
    def _validate_inputs(compute_config_location: str):
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

    def _generate_client(self):
        """
        Generate the client for the compute instance.
        """
        client_builder = {
            "ec2": self._create_aws_client,
            "avm": self._create_azure_client,
            "gce": self._create_gcp_client,
        }

        if self.compute_type in client_builder:
            return client_builder[self.compute_type]()
        else:
            raise ValueError(f"Invalid instance_type: {self.compute_type}")

    def _create_aws_client(self):
        """
        Create the AWS client.

        Returns:
            boto3.client
        """
        return boto3.client("ec2", **self._auth_config.dict())

    def _create_azure_client(self):
        """
        Create the Azure client.

        Returns:
            ComputeManagementClient
        """
        credential = ClientSecretCredential(**self._auth_config.dict())

        return ComputeManagementClient(credential, self._auth_config["subscription_id"])

    def _create_gcp_client(self):
        """
        Create the GCP client.

        Returns:
            compute.ComputeClient
        """
        credentials = service_account.Credentials.from_service_account_file(
            self._auth_config["credentials"]
        )
        return compute.ComputeClient(credentials=credentials)

    def _build_ec2_instance(self, config: EC2Config):
        instance = self._client.create_instances(
            ImageId=self.get_latest_AMI_id(config.image_id, config.region_name),
            MinCount=config.min_instance_count,
            MaxCount=config.max_instance_count,
            InstanceType=config.instance_type,
            KeyName=self._generate_ec2_key_pair(config.key_name),
            SecurityGroupIds=config.security_group_ids,
        )
        return instance[0].id  # return instance id

    def _generate_ec2_key_pair(self, key_name: str):
        key_pair = self._client.create_key_pair(KeyName=key_name)
        with open(f"{key_name}.pem", "w") as file:
            file.write(key_pair.key_material)
        return key_name

    @staticmethod
    def get_latest_AMI_id(ami_path: str, region_name: str):
        ssm = boto3.client("ssm", region_name=region_name)
        response = ssm.get_parameter(Name=ami_path, WithDecryption=True)
        return response["Parameter"]["Value"]

    def _build_gce_instance(self, config: GCEConfig):
        instance = self._client.insert(
            project=config.project,
            zone=config.zone,
            body={
                "name": config.name,
                "machineType": f"zones/{config.zone}/machineTypes/{config.machine_type}",
                "disks": [
                    {
                        "initializeParams": {
                            "diskSizeGb": config.disk_size,
                            "sourceImage": "projects/debian-cloud/global/images/family/debian-9",  # sample image
                        },
                        "boot": True,
                        "autoDelete": True,
                    },
                ],
            },
        )
        return instance.operation.name  # return operation name

    def _build_avm_instance(self, config: AVMConfig):
        vm_parameters = {
            "location": config.location,
            "hardware_profile": {"vm_size": config.size},
            # Define other parameters here...
        }
        operation = self._client.virtual_machines.create_or_update(
            config.resource_group_name, config.vm_name, vm_parameters
        )
        operation.wait()
