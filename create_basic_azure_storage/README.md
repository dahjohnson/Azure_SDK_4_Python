# Create an Azure Storage Account

## Create the virtual environment

### `python3 -m venv .venv`

## Activate the virtual environment

### `.source .venv/bin/activate`

## Install requirements

### `pip install -r requirements.txt`

## Export Azure Sub ID to environment variable

### `export AZURE_SUB_ID=$(az account show | jq -r '.id')`

## Create Storage Account

### `python create_storage_account.py`

## Clean up

### `az group delete -n <Resource_Group_Name> --no-wait

## Deactivate virtual environment

### `deactivate`
