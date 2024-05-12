# OFB Python SDK

The `ofb-python-sdk` provides a Python interface for interacting with Microsoft's OneDrive. It simplifies the process of authenticating, uploading, downloading, and managing files on OneDrive through a simple and intuitive API. This SDK is particularly useful for developers who need to integrate OneDrive functionalities within their Python applications efficiently.

## Features

- Authentication with OAuth2
- Upload files to OneDrive (supports both small and large files)
- Download files from OneDrive
- Create and manage folders
- Delete files and folders
- Handle file conflicts with customizable behavior
- Rich progress bar integration for file uploads

## Installation

Install `ofb-python-sdk` using pip:

```bash
pip install sy-ofb-python-sdk
```

## Usage

To start using the SDK, you'll first need to import the `Client` class from the package.

```python
from ofb_python_sdk import Client
```

### Setup

Initialize the client with your application credentials:

```python
client = Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token",
    redirect_uri="your_redirect_uri",
)
```

### Upload a File

```python
file_path = "/path/to/your/file"
file_data = open(file_path, "rb").read()
remote_path = "/path/to/onedrive/destination/file.txt"

try:
    response = client.upload_file(file_data, remote_path)
    print("Upload successful:", response.status_code)
except Exception as e:
    print("Upload failed:", e)
```

### Download a File

```python
remote_path = "/path/to/onedrive/file.txt"

try:
    file_data = client.download_file(remote_path)
    with open("downloaded_file.txt", "wb") as file:
        file.write(file_data)
    print("Download successful")
except Exception as e:
    print("Download failed:", e)
```

### Create a Folder

```python
folder_path = "/new/folder"

try:
    response = client.create_folder(folder_path)
    print("Folder creation successful:", response.status_code)
except Exception as e:
    print("Folder creation failed:", e)
```

### Delete a File

```python
remote_path = "/path/to/delete/file.txt"

try:
    response = client.delete_file(remote_path)
    print("Deletion successful:", response.status_code)
except Exception as e:
    print("Deletion failed:", e)
```

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you need assistance or encounter any bugs, please open an issue on the project's [GitHub issues page](https://github.com/shing-yu/ofb-python-sdk/issues).
