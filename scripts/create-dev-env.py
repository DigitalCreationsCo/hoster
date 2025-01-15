import os
import subprocess

def config(key, default=None):
    """Fetch configuration value from environment or return default."""
    return os.getenv(key, default)

def fetch_azure_value(key):
    """Fetch value from Azure CLI."""
    try:
        result = subprocess.run(
            ["az", "config", "get-value", key],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def fetch_terraform_value(key):
    """Fetch value from Terraform state."""
    try:
        result = subprocess.run(
            ["terraform", "output", key],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def write_to_env_file(env_vars, env):
    """Write environment variables to .env file."""
    with open(env, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    print(".env file has been populated.")


# DEV VARIABLES
def create_dev_env():
    """Populate .env.dev file with development-specific values."""
    env_vars = {}

    env_vars["IS_PRODUCTION"] = config("IS_PRODUCTION", default="False")

    env_vars["AZURE_CLIENT_ID"] = fetch_azure_value("AZURE_CLIENT_ID") or config("AZURE_CLIENT_ID", default="")
    env_vars["AZURE_TENANT_ID"] = fetch_azure_value("AZURE_TENANT_ID") or config("AZURE_TENANT_ID", default="")
    env_vars["AZURE_SUBSCRIPTION_ID"] = fetch_azure_value("AZURE_SUBSCRIPTION_ID") or config("AZURE_SUBSCRIPTION_ID", default="")
    env_vars["AZURE_CREDENTIALS"] = config("AZURE_CREDENTIALS")
 
    env_vars["AZURE_LOCATION"] = fetch_azure_value("AZURE_LOCATION") or config("AZURE_LOCATION", default="eastasia")
    env_vars["AZURE_STORAGE_ACCOUNT_NAME"] = fetch_azure_value("AZURE_STORAGE_ACCOUNT_NAME") or config("AZURE_STORAGE_ACCOUNT_NAME", default="tfstate00002")
    env_vars["AZURE_STORAGE_CONNECTION_STRING"] = fetch_azure_value("AZURE_STORAGE_CONNECTION_STRING") or config("AZURE_STORAGE_CONNECTION_STRING", default="")
    env_vars["AZURE_CONTAINER_NAME"] = fetch_azure_value("AZURE_CONTAINER_NAME") or config("AZURE_CONTAINER_NAME", default="projects")
    env_vars["AZURE_STORAGE_ACCOUNT_KEY"] = fetch_azure_value("AZURE_STORAGE_ACCOUNT_KEY", ["az", "storage", "account", "keys", "list", "--account-name", "tfstate00002", "--resource-group", "hoster", "--query", "[0].value"]) or config("AZURE_STORAGE_ACCOUNT_KEY", default="")

    env_vars["AZURE_APP_SERVICE_NAME"] = fetch_azure_value("AZURE_APP_SERVICE_NAME") or config("AZURE_APP_SERVICE_NAME", default="hoster")
    env_vars["AZURE_RESOURCE_GROUP"] = fetch_azure_value("AZURE_RESOURCE_GROUP") or config("AZURE_RESOURCE_GROUP", default="hoster")
    env_vars["STORAGE_BACKEND"] = config("STORAGE_BACKEND", default="azure")

    env_vars["DEBUG"] = "True"  # Set DEBUG to True for development
    env_vars["DEFAULT_SECRET"] = "default-dev-secret-key"
    env_vars["SECRET_KEY"] = "dev-secret-key"  # Use a different key for development

    env_vars["POSTGRES_DATABASE"] = "dev_db"  # Use a development database
    env_vars["POSTGRES_USERNAME"] = "dev_user"
    env_vars["POSTGRES_PASSWORD"] = "dev_password"
    env_vars["POSTGRES_HOST"] = "localhost"  # Use local database for dev
    env_vars["POSTGRES_PORT"] = "5432"

    env_vars["APPLICATIONINSIGHTS_CONNECTION_STRING"] = fetch_azure_value("APPLICATIONINSIGHTS_CONNECTION_STRING")

    env_vars["WEBSITE_HOSTNAME"] = "localhost:5173"
    env_vars["BACKEND_URL"] = ""

    if os.getenv("CODESPACE_NAME"):
        env_vars["GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN"] = os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN', '')

    # Fetch additional values from Terraform if needed (for development)
    # terraform_key = "your_terraform_output_key"
    # terraform_value = fetch_terraform_value(terraform_key)
    # if terraform_value:
    #     env_vars[terraform_key] = terraform_value

    # Write the environment variables to the .env file for development
    write_to_env_file(env_vars, ".env")

if __name__ == "__main__":
    create_dev_env()
