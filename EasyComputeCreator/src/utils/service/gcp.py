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
    AVMConfig,
    AzureAccessKey, GCEConfig, GCPAccessKey,
)
from src.utils.service.base import Client

logger = logging.getLogger(__name__)


class GCPClient(Client):
    @property
    def client(self) -> compute.ComputeClient:
        """
        Create the GCP client.

        Returns:
            compute.ComputeClient
        """
        credentials = service_account.Credentials.from_service_account_file(
            self._auth_config["credentials"]
        )
        return compute.ComputeClient(credentials=credentials)

    def build_compute_instance(self):
        instance = self.client.insert(
            project=self._compute_config.project,
            zone=self._compute_config.zone,
            body={
                "name": self._compute_config.name,
                "machineType": f"zones/{self._compute_config.zone}/machineTypes/{self._compute_config.machine_type}",
                "disks": [
                    {
                        "initializeParams": {
                            "diskSizeGb": self._compute_config.disk_size,
                            "sourceImage": "projects/debian-cloud/global/images/family/debian-9",  # sample image
                        },
                        "boot": True,
                        "autoDelete": True,
                    },
                ],
            },
        )
        return instance.operation.name  # return operation name