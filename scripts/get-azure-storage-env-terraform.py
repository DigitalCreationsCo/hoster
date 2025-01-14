import json

# Load Terraform outputs
with open('terraform_outputs.json', 'r') as file:
    outputs = json.load(file)

# Extract values
azure_connection_string = outputs['azure_connection_string']['value']
azure_container_name = outputs['azure_container_name']['value']

# Write to .env file
with open('.env', 'w') as env_file:
    env_file.write(f"AZURE_STORAGE_CONNECTION_STRING={azure_connection_string}\n")
    env_file.write(f"AZURE_CONTAINER_NAME={azure_container_name}\n")
    env_file.write("STORAGE_BACKEND=azure\n")
