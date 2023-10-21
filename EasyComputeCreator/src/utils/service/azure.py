import logging
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from src.utils.service.base import Client

logger = logging.getLogger(__name__)


class AzureClient(Client):
    @property
    def client(self) -> ComputeManagementClient:
        """
        Create the Azure client.

        Returns:
            ComputeManagementClient
        """
        credential = ClientSecretCredential(**self._auth_config.dict())

        return ComputeManagementClient(credential, self._auth_config["subscription_id"])

    def build_compute_instance(self):
        vm_parameters = {
            "location": self._compute_config.location,
            "hardware_profile": {"vm_size": self._compute_config.size},
        }
        operation = self.client.virtual_machines.create_or_update(
            self._compute_config.resource_group_name, self._compute_config.vm_name, vm_parameters
        )
        operation.wait()