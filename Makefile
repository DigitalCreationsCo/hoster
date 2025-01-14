.PHONY: init generate-env setup build-backend build-frontend deploy-backend deploy-frontend verify-logs clean-infra

# Initialize the project and deploy infrastructure
init:
	@echo "Initializing and applying Terraform configuration..."
	cd infra && terraform init && terraform apply -auto-approve

# Populate .env file from Terraform outputs
generate-env:
	@echo "Running create-env.py..."
	python ../scripts/create-dev-env.py
	@echo "Generating .env file from Terraform outputs..."
	cd infra && terraform output -json | python ../scripts/get-azure-storage-env-terraform.py

# Full setup: Initialize Terraform, deploy, and generate .env
setup: init generate-env
	@echo "Setup complete. .env file generated."

build-backend:
	cd backend && python manage.py collectstatic --noinput

build-frontend:
	cd frontend && npm install && npm run build

deploy-backend:
	azd deploy --service backend

deploy-frontend:
	cd frontend && az storage blob upload-batch \
	    --source dist \
	    --destination '$$(az storage account show --name $(AZURE_STORAGE_ACCOUNT_NAME) --query primaryEndpoints.web -o tsv)' \
	&& make update-frontend-env

update-frontend-env:
	@echo "Updating .env file with Frontend URL..."
	@WEBSITE_HOSTNAME=$$(az storage account show --name $(AZURE_STORAGE_ACCOUNT_NAME) --query primaryEndpoints.web -o tsv)
	@echo "WEBSITE_HOSTNAME=$$WEBSITE_HOSTNAME" >> .env.prod
	@echo "Frontend URL: $$WEBSITE_HOSTNAME"

verify-logs:
	az webapp log tail --name $(AZURE_APP_SERVICE_NAME) --resource-group $(AZURE_RESOURCE_GROUP)

# Clean up Terraform state and outputs
clean-infra:
	@echo "Cleaning up Terraform state and outputs..."
	cd infra && terraform destroy -auto-approve && rm -f terraform_outputs.json
	@echo "Cleanup complete."
