import pytest
from unittest import mock
from unittest.mock import MagicMock
from botocore.exceptions import BotoCoreError, ClientError
from google.auth.exceptions import GoogleAuthError
from msrest.exceptions import AuthenticationError
from src.compute_creator import ComputeCreator


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("COMPUTE_CONFIG_LOCATION", "tests/test_data/compute_config.yaml")


def test_compute_creator_init(mock_env):
    cc = ComputeCreator()
    assert cc.compute_name == "test_compute"
    assert cc.compute_type == "ec2"
    assert isinstance(cc.compute_config, dict)
    assert isinstance(cc._auth_config, dict)


def test_compute_creator_init_invalid_yaml():
    with pytest.raises(Exception) as exception_info:
        cc = ComputeCreator(compute_config_location="tests/test_data/invalid.yaml")
    assert str(exception_info.value) == "Validation failed. Error: ...."


@mock.patch("src.compute_creator.boto3.client")
def test_generate_client_ec2(boto3_mock):
    cc = ComputeCreator()
    cc.compute_type = "ec2"
    cc._generate_client()
    boto3_mock.assert_called_once()


@mock.patch("src.compute_creator.ClientSecretCredential")
@mock.patch("src.compute_creator.ComputeManagementClient")
def test_generate_client_avm(credential_mock, compute_manager_mock):
    cc = ComputeCreator()
    cc.compute_type = "avm"
    cc._generate_client()
    credential_mock.assert_called_once()
    compute_manager_mock.assert_called_once()


@pytest.mark.parametrize(
    "ptype, service_account",
    [("gce", "test/account.json"), ("ec2", "invalid"), ("avm", "invalid")],
)
def test_generate_client_raises_error(ptype, service_account, mock_env):
    cc = ComputeCreator()
    cc._auth_config = {"credentials": service_account}
    cc.compute_type = ptype

    with pytest.raises(ValueError):
        cc._generate_client()


@mock.patch("src.compute_creator.ComputeCreator._create_aws_client")
def test_build_aws(client_mock):
    cc = ComputeCreator()
    cc.compute_type = "ec2"
    cc.build()
    client_mock.assert_called_once()


@mock.patch("src.compute_creator.ComputeCreator._create_gcp_client")
def test_build_gcp(client_mock):
    cc = ComputeCreator()
    cc.compute_type = "gce"
    cc.build()
    client_mock.assert_called_once()


@mock.patch("src.compute_creator.ComputeCreator._create_azure_client")
def test_build_avm(client_mock):
    cc = ComputeCreator()
    cc.compute_type = "avm"
    cc.build()
    client_mock.assert_called_once()


def test_build_unknown_type():
    cc = ComputeCreator()
    cc.compute_type = "invalid"
    with pytest.raises(ValueError):
        cc.build()
