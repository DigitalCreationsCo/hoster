import os
import subprocess

def config(key, default=None):
    """Fetch configuration value from environment or return default."""
    return os.getenv(key, default)

def fetch_azure_value(key, azure_cli_command):
    """Fetch value from Azure CLI."""
    try:
        result = subprocess.run(
            azure_cli_command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Error fetching {key} from Azure CLI.")
        return None

def write_to_env_file(env_vars, env):
    """Write environment variables to .env file."""
    with open(env, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    print(".env file has been populated.")

# PRODUCTION VARIABLES
def create_prod_env():
    """Populate .env file with values from environment, Azure, Terraform, etc."""
    env_vars = {}

    env_vars["IS_PRODUCTION"] = config("IS_PRODUCTION", default="True")

    env_vars["AZURE_CLIENT_ID"] = config("AZURE_CLIENT_ID")
    env_vars["AZURE_TENANT_ID"] = config("AZURE_TENANT_ID")
    env_vars["AZURE_SUBSCRIPTION_ID"] = config("AZURE_SUBSCRIPTION_ID")
    env_vars["AZURE_CREDENTIALS"] = config("AZURE_CREDENTIALS")
    
    env_vars["AZURE_LOCATION"] = fetch_azure_value("AZURE_LOCATION", ["az", "group", "list", "--query", "[0].location", "-o", "tsv"]) or config("AZURE_LOCATION", default="eastus")
    env_vars["AZURE_STORAGE_ACCOUNT_NAME"] = fetch_azure_value("AZURE_STORAGE_ACCOUNT_NAME", ["az", "storage", "account", "list", "--query", "[0].name", "-o", "tsv"]) or config("AZURE_STORAGE_ACCOUNT_NAME", default="tfstate00002")
    env_vars["AZURE_STORAGE_CONNECTION_STRING"] = fetch_azure_value("AZURE_STORAGE_CONNECTION_STRING", ["az", "storage", "account", "show-connection-string", "--name", "tfstate00002", "--resource-group", "hoster", "--query", "connectionString"]) or config("AZURE_STORAGE_CONNECTION_STRING")

    env_vars["AZURE_CONTAINER_NAME"] = config("AZURE_CONTAINER_NAME", default="projects")
    env_vars["AZURE_STORAGE_ACCOUNT_KEY"] = fetch_azure_value("AZURE_STORAGE_ACCOUNT_KEY", ["az", "storage", "account", "keys", "list", "--account-name", "tfstate00002", "--resource-group", "hoster", "--query", "[0].value"]) or config("AZURE_STORAGE_ACCOUNT_KEY")

    env_vars["AZURE_APP_SERVICE_NAME"] = config("AZURE_APP_SERVICE_NAME", default="hoster")
    env_vars["AZURE_RESOURCE_GROUP"] = config("AZURE_RESOURCE_GROUP", default="hoster")
    env_vars["STORAGE_BACKEND"] = config("STORAGE_BACKEND", default="azure")

    env_vars["DEBUG"] = "False"
    env_vars["DEFAULT_SECRET"] = "default-secret"
    env_vars["SECRET_KEY"] = config("SECRET_KEY", default=env_vars["DEFAULT_SECRET"])

    # Database variables are provided by Actions pipeline
    # env_vars["POSTGRES_DATABASE"] = config("POSTGRES_DATABASE")
    # env_vars["POSTGRES_USERNAME"] = config("POSTGRES_USERNAME")
    # env_vars["POSTGRES_PASSWORD"] = config("POSTGRES_PASSWORD")
    # env_vars["POSTGRES_HOST"] = config("POSTGRES_HOST")
    # env_vars["POSTGRES_PORT"] = config("POSTGRES_PORT", default=5432)

    env_vars["WEBSITE_HOSTNAME"] = "https://tfstate00002.blob.core.windows.net/$web"
    env_vars["BACKEND_URL"] = "placeholder-backend-url"
    # Write the environment variables to the .env file
    write_to_env_file(env_vars, ".env.production")

if __name__ == "__main__":
    create_prod_env()
