#!/bin/bash

echo "Verifying frontend deployment..."
az storage blob list --account-name $AZURE_STORAGE_ACCOUNT_NAME --container-name '$web'

echo "Verifying backend deployment logs..."
az webapp log tail --name $AZURE_APP_SERVICE_NAME --resource-group $AZURE_RESOURCE_GROUP
