from django.conf import settings
import mimetypes
import zipfile
import os
import mimetypes
from io import BytesIO
from datetime import datetime, timedelta

from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, ServiceRequestError
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

class AzureStorageBackend:
    def __init__(self):
        try:
            print('azure storage connection string')
            print (settings.AZURE_STORAGE_CONNECTION_STRING)
            self.client = BlobServiceClient.from_connection_string(
                settings.AZURE_STORAGE_CONNECTION_STRING, 
            )
            self.container_name = settings.AZURE_CONTAINER_NAME
            self.account_name = settings.AZURE_STORAGE_ACCOUNT_NAME
            self.account_key = settings.AZURE_STORAGE_ACCOUNT_KEY
            
            print(self.container_name)
            # Verify container exists
            self.client.get_container_client(settings.AZURE_CONTAINER_NAME).get_container_properties()
        except ResourceNotFoundError:
            raise ValueError(f"Container {self.container_name} not found")
        except Exception as e:
            raise ValueError(f"Failed to initialize storage client: {str(e)}")

    def _upload_file(self, file, file_name):
        """Uploads an individual file to Azure Blob Storage."""
        try:
            blob_client = self.client.get_blob_client(
                container=self.container_name, 
                blob=file_name
            )

            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                mime_type = 'application/octet-stream'  # Default fallback

            content_settings = ContentSettings(content_type=mime_type)

            # Upload the file
            blob_client.upload_blob(file, overwrite=True, content_settings=content_settings)

            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container_name,
                blob_name=file_name,
                account_key=self.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )

            # Return URL with SAS token
            url = f"{blob_client.url}?{sas_token}"
            return url
        
        except ResourceExistsError:
            raise ValueError(f"File {file_name} already exists")
        except ServiceRequestError:
            raise ValueError("Failed to connect to Azure Storage")
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")

    def _upload_folder(self, folder_path, folder_name):
        """Uploads a folder (including subdirectories) to Azure Blob Storage."""
        try:
            # Walk through the folder
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    # Get the relative path of the file
                    relative_path = os.path.relpath(os.path.join(root, file_name), folder_path)
                    # Upload file
                    with open(os.path.join(root, file_name), 'rb') as file:
                        file_url = self._upload_file(file, f"{folder_name}/{relative_path}")
                        print(f"File uploaded: {file_url}")
        except Exception as e:
            raise ValueError(f"Failed to upload folder {folder_name}: {str(e)}")

    def _upload_zip(self, zip_file, folder_name):
        """Unzips and uploads files from a ZIP archive to Azure Blob Storage."""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Iterate over each file in the ZIP archive
                for zip_file_name in zip_ref.namelist():
                    # Handle directories in the ZIP by creating a corresponding folder in the container
                    if zip_file_name.endswith('/'):
                        continue  # Skip directories
                    file_content = zip_ref.read(zip_file_name)
                    file_url = self._upload_file(BytesIO(file_content), f"{folder_name}/{zip_file_name}")
                    print(f"File uploaded from ZIP: {file_url}")
        except zipfile.BadZipFile:
            raise ValueError("Provided file is not a valid ZIP file.")
        except Exception as e:
            raise ValueError(f"Failed to upload ZIP contents: {str(e)}")

    def upload_file(self, file, file_name, is_zip=False):
        """Uploads a file (or folder/ZIP) to Azure Blob Storage."""
        try:
            if is_zip:
                # If it's a zip file, unzip and upload
                self._upload_zip(file, file_name)
            elif os.path.isdir(file_name):
                # If it's a directory, upload the entire folder
                self._upload_folder(file_name, file_name)
            else:
                # If it's a single file, upload it directly
                return self._upload_file(file, file_name)
        except Exception as e:
            raise ValueError(f"Failed to upload: {str(e)}")

class StorageService:
    @staticmethod
    def get_storage_backend():
        try:
            if settings.STORAGE_BACKEND == 'azure':
                return AzureStorageBackend()
            else:
                raise NotImplementedError("Unsupported storage backend")
        except Exception as e:
            raise ValueError(f"Failed to initialize storage service: {str(e)}")