---
page_type: sample
languages:
- react
- python
- azure-cli
- github-actions
products:
- azure
- azure-app-service
- azure-database-postgresql
urlFragment: django-react-azure-deployment
name: Deploy Django + React Application with PostgreSQL on Azure
---

# Deploy Django + React Application with PostgreSQL on Azure

This project deploys a full-stack web application with a Django backend and React frontend. It leverages Azure services for hosting and includes infrastructure automation with Azure Developer CLI (azd) and GitHub Actions.

## Project Features

- **Frontend Deployment**: React app hosted on Azure Blob Storage.
- **Backend Deployment**: Django app hosted on Azure App Service.
- **Database**: Azure PostgreSQL integrated with the Django application.
- **Infrastructure Automation**: Azure resources provisioned using azd and GitHub workflows.
- **Traffic Management**: Azure Application Gateway configured to route traffic efficiently.

## Running the Project Locally

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory and set up the backend:
   ```sh
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set environment variables for the PostgreSQL database:
   ```sh
   export POSTGRES_HOST=<host>
   export POSTGRES_PORT=<port>
   export POSTGRES_DATABASE=<database_name>
   export POSTGRES_USERNAME=<username>
   export POSTGRES_PASSWORD=<password>
   ```
4. Apply database migrations and seed data:
   ```sh
   python3 manage.py migrate
   python3 manage.py loaddata seed_data.json
   ```
5. Start the backend server:
   ```sh
   python3 manage.py runserver 8000
   ```
6. Navigate to the frontend directory and run the React app:
   ```sh
   cd ../frontend
   npm install
   npm start
   ```

## Deployment Steps

### Prerequisites

1. Sign up for an [Azure account](https://azure.microsoft.com/free/).
2. Install the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).
3. Authenticate with Azure:
   ```sh
   azd auth login

   Here's a section you can add to your `README.md` to explain the functionality of `create-prod-env.py` and `master_hoster.yml`:

---

## Automatic .env Creation and Azure Integration in GitHub Actions

### Overview
This project includes an automated workflow for setting up the environment variables needed for running the development server and deploying the project in production. The following functionality is provided:

- **create-dev-env.py**: A Python script that fetches development-environment-specific values directly from Azure using the Azure CLI and creates a `.env` file with the necessary configurations.
- **create-prod-env.py**: A Python script that fetches production-environment-specific values directly from Azure using the Azure CLI and creates a `.env.production` file with the necessary configurations.
- **GitHub Actions Workflow (master_hoster.yml)**: An automated workflow that runs on GitHub Actions to set up the environment, fetch Azure credentials, and deploy the application to Azure Web Apps and Azure Blob Storage.

### `create-prod-env.py` Script

The `create-prod-env.py` script is responsible for generating a `.env.production` file by pulling the required environment variables from multiple sources:

1. **Environment Variables**: It first checks if any environment variables (such as `IS_PRODUCTION`, `SECRET_KEY`, etc.) are set locally or in the workflow.
2. **Azure CLI**: The script fetches key configuration values from Azure directly using the Azure CLI. These values include:
   - **Azure Subscription ID**
   - **Azure Tenant ID**
   - **Azure Client ID**
   - **Azure Resource Group**
   - **Azure Storage Account Information**
   - **Azure Location**
   
   The script uses the Azure CLI commands to retrieve these values. For example, it retrieves the Azure Tenant ID with the command `az account show --query tenantId`.

3. **Database Configuration**: The script also checks for database credentials (such as PostgreSQL host, username, password, etc.) from environment variables.

4. **Other Configuration**: Default values for secrets and environment variables are set if not provided.

The script then writes all these values into a `.env.production` file, which is used later in the deployment process to configure the application environment.

### `master_hoster.yml` GitHub Actions Workflow

The `master_hoster.yml` file defines the CI/CD pipeline for building and deploying the application. It consists of the following jobs:

1. **build-backend**:
   - This job sets up a Python environment on an Ubuntu runner, installs the required dependencies, and runs the `create-prod-env.py` script.
   - It authenticates with Azure using a service principal (via the `azure/login` action).
   - After fetching the required values from Azure and generating the `.env.production` file, it zips the application and prepares it for deployment.
   
2. **build-frontend**:
   - This job handles the frontend build process. It sets up a Node.js environment, installs frontend dependencies, and builds the frontend application.
   - The built frontend is then uploaded as an artifact.

3. **deploy**:
   - This job deploys the backend to Azure Web App and the frontend to Azure Blob Storage.
   - The `.env.production` file generated earlier is included in the deployment, ensuring that all the necessary environment variables are available during the deployment process.

### Workflow Execution

Whenever code is pushed to the `master` branch, or the workflow is manually triggered, the following steps occur:

1. **Azure Login**: The `azure/login` action authenticates to Azure using the service principal credentials stored in GitHub Secrets.
2. **.env Generation**: The `create-prod-env.py` script is executed to fetch Azure resource details and generate the `.env.production` file.
3. **Build**: The backend and frontend are built, zipped, and uploaded as artifacts.
4. **Deployment**: The backend is deployed to Azure Web App, and the frontend is uploaded to Azure Blob Storage for static content hosting.

### Azure CLI Permissions

To enable seamless Azure CLI commands execution in GitHub Actions, ensure the service principal has the following permissions:

- **Reader** or **Contributor** role on the subscription or resource group to retrieve the necessary configuration (like `tenantId`, `subscriptionId`, etc.).
- **Storage Blob Data Contributor** role to upload the frontend bundle to Azure Blob Storage.

By automating these tasks, this setup ensures a streamlined production deployment with all necessary Azure configuration automatically pulled from the Azure environment and securely handled within the workflow.

Managing Sensitive Variables with Azure Key Vault
Overview
For handling sensitive environment variables such as database credentials, API keys, and other secrets, we use Azure Key Vault. Azure Key Vault allows you to securely store and manage sensitive information and provides mechanisms for retrieving these values in a controlled and auditable manner.

In this project, sensitive variables are stored in Azure Key Vault and fetched securely during the GitHub Actions workflow. The variables are used to populate the environment and ensure secure deployment to Azure.

Setting Up Azure Key Vault
Create an Azure Key Vault: If you don't already have an Azure Key Vault, create one using the Azure CLI or the Azure portal.

Example command to create a Key Vault:

bash
Copy code
az keyvault create --name <YourKeyVaultName> --resource-group <YourResourceGroup> --location <YourAzureRegion>
Store Secrets: Secrets (such as database passwords, client secrets, etc.) can be stored in the Key Vault. You can add secrets using the Azure CLI, PowerShell, or the Azure portal.

Example command to add a secret:

bash
Copy code
az keyvault secret set --vault-name <YourKeyVaultName> --name <SecretName> --value <SecretValue>
Service Principal Permissions: The service principal used in the GitHub Actions workflow must have get permissions for the Key Vault to be able to retrieve the secrets.

Example command to grant get permissions:

bash
Copy code
az keyvault set-policy --name <YourKeyVaultName> --spn <YourServicePrincipalID> --secret-permissions get
Fetching Secrets in GitHub Actions
During the GitHub Actions workflow, sensitive variables such as database passwords or client secrets are securely fetched from Azure Key Vault. This is done using the Azure CLI in combination with the az keyvault secret show command.

The key steps in the workflow are as follows:

Authenticate with Azure: The azure/login GitHub Action authenticates with Azure using a service principal. The necessary Azure credentials (client-id, tenant-id, and client-secret) are stored in GitHub Secrets and used to authenticate.

yaml
Copy code
- name: Log in to Azure
  uses: azure/login@v1
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    secret: ${{ secrets.AZURE_CLIENT_SECRET }}
Fetch Secrets from Azure Key Vault: Once authenticated, the workflow fetches secrets from Azure Key Vault using the az keyvault secret show command. For example, to fetch a secret named POSTGRES_PASSWORD from the Key Vault:

yaml
Copy code
- name: Fetch PostgreSQL password from Azure Key Vault
  run: |
    export POSTGRES_PASSWORD=$(az keyvault secret show --name POSTGRES_PASSWORD --vault-name <YourKeyVaultName> --query value -o tsv)
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> $GITHUB_ENV
This command fetches the POSTGRES_PASSWORD from the specified Key Vault and exports it as an environment variable that can be used in subsequent steps of the workflow.

Secure Usage: The secrets are used securely in the workflow, ensuring they are never exposed in logs or stored in code. The environment variables are passed to the deployment steps, where they are needed.

Example of Fetching Multiple Secrets: You can use the following pattern to fetch multiple secrets from Azure Key Vault and set them as environment variables:

yaml
Copy code
- name: Fetch secrets from Azure Key Vault
  run: |
    export POSTGRES_PASSWORD=$(az keyvault secret show --name POSTGRES_PASSWORD --vault-name <YourKeyVaultName> --query value -o tsv)
    export AZURE_STORAGE_KEY=$(az keyvault secret show --name AZURE_STORAGE_KEY --vault-name <YourKeyVaultName> --query value -o tsv)
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> $GITHUB_ENV
    echo "AZURE_STORAGE_KEY=$AZURE_STORAGE_KEY" >> $GITHUB_ENV
Benefits of Using Azure Key Vault
Security: Sensitive data is stored securely, and access is tightly controlled.
Auditability: All access to the Key Vault is logged, allowing you to track who accessed the secrets and when.
Centralized Management: You can manage all sensitive variables in one place, making it easier to rotate secrets and manage access permissions.
Seamless Integration with Azure: Azure Key Vault integrates smoothly with Azure services, making it a powerful tool for cloud-native applications.
Additional Configuration
If you need to fetch secrets from Azure Key Vault during your workflow, ensure that the service principal used by the GitHub Actions workflow has the appropriate permissions:

Assign get permissions to the service principal for the Key Vault.
Set up GitHub Secrets: Store the AZURE_CLIENT_ID, AZURE_TENANT_ID, and AZURE_CLIENT_SECRET in GitHub Secrets to authenticate the service principal.
By using Azure Key Vault, you can manage sensitive data securely without exposing it in the GitHub Actions workflow, ensuring your deployment process remains both secure and automated.

### Deployment Process

1. Initialize the azd project:
   ```sh
   azd init
   ```
2. Provision resources and deploy the application:
   ```sh
   azd up
   ```
   Follow the prompts to provide an environment name, Azure subscription, and resource location.

3. For subsequent deployments after code changes:
   ```sh
   azd deploy
   ```

### CI/CD Pipeline

This project includes GitHub workflows for automatic deployments. To configure:

1. Run the following command to set up pipeline secrets:
   ```sh
   azd pipeline config
   ```
2. Push your changes to the `main` branch to trigger the workflow.

## Additional Notes

- **Terraform Support**: Terraform scripts are included for infrastructure setup but require a compatible environment with `azure-cli` installed.
- **Live Application**: Access the live app [here](Insert-live-link).

---

For any issues or questions, feel free to contact Bryant Mejia at bryantmejia722@outlook.com.
