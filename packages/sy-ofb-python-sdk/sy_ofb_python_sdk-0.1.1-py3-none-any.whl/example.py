from ofb_python_sdk import Client

client_id = "your client id"
client_secret = "your client secret"
refresh_token = "your refresh token"
redirect_uri = "your redirect uri"

app = Client(client_id, client_secret, refresh_token, redirect_uri)

# Upload a file
app.upload_file("Hello, World!".encode("utf-8"), "/test.txt")

# Upload a big file
app.upload_big_file("Hello, World!".encode("utf-8"), "/testbig.txt")

# create a folder
app.create_folder("/test")

# download a file
file = app.download_file("/test.txt")
print(file.decode("utf-8"))

# move a file to recycle bin
app.delete_file("/test.txt")
