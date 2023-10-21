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
    EC2Config,
    AWSAccessKey,
)
from src.utils.service.base import Client

logger = logging.getLogger(__name__)


class AWSClient(Client):
    @property
    def client(self) -> boto3.client:
        """
        Create the AWS client.

        Returns:
            boto3.client
        """
        return boto3.client("ec2", **self._auth_config.dict())

    def build_compute_instance(self):
        instance = self.client.create_instances(
            ImageId=self.get_latest_AMI_id(self._compute_config.image_id, self._compute_config.region_name),
            MinCount=self._compute_config.min_instance_count,
            MaxCount=self._compute_config.max_instance_count,
            InstanceType=self._compute_config.instance_type,
            KeyName=self._generate_ec2_key_pair(self._compute_config.key_name),
            SecurityGroupIds=self._compute_config.security_group_ids,
        )
        return instance[0].id  # return instance id

    def _generate_ec2_key_pair(self, key_name: str):
        key_pair = self.client.create_key_pair(KeyName=key_name)
        with open(f"{key_name}.pem", "w") as file:
            file.write(key_pair.key_material)
        return key_name

    @staticmethod
    def get_latest_AMI_id(ami_path: str, region_name: str):
        ssm = boto3.client("ssm", region_name=region_name)
        response = ssm.get_parameter(Name=ami_path, WithDecryption=True)
        return response["Parameter"]["Value"]
