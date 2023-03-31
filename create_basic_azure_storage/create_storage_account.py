import os, random

from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

credential = AzureCliCredential()

subscription_id = os.environ["AZURE_SUB_ID"]

resource_client = ResourceManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "Python-SDK-Storage-RG"
LOCATION = "eastus"

rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
    { "location": LOCATION })

print(f"Provisioned resource group {rg_result.name}")

storage_client = StorageManagementClient(credential, subscription_id)

STORAGE_ACCOUNT_NAME = f"azpythonsdk{random.randint(1,100):05}storage"

availability_result = storage_client.storage_accounts.check_name_availability(
    { "name": STORAGE_ACCOUNT_NAME }
)

if not availability_result.name_available:
    print(f"Storage name {STORAGE_ACCOUNT_NAME} is not available. Try another name. Storage account name must be between 3 and 24 characters in length and use numbers and lower-case letters only.")
    exit()

poller = storage_client.storage_accounts.begin_create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME,
    {
        "location" : LOCATION,
        "kind": "StorageV2",
        "sku": {"name": "Standard_LRS"}
    }
)

account_result = poller.result()
print(f"Provisioned storage account {account_result.name}")

keys = storage_client.storage_accounts.list_keys(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME)

print(f"Primary key for storage account: {keys.keys[0].value}")

conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={keys.keys[0].value}"

print(f"Connection string: {conn_string}")

CONTAINER_NAME = "blob-container-01"
container = storage_client.blob_containers.create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, CONTAINER_NAME, {})

print(f"Provisioned blob container {container.name}")
