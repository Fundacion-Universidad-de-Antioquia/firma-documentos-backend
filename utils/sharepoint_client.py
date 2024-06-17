from shareplum import Site
from shareplum import Office365

# SharePoint site credentials
site_url = "https://<url>"
username = "username"
password = "password"

# Connect to SharePoint site
authcookie = Office365(site_url, username=username, password=password).GetCookies()
site = Site(site_url, authcookie=authcookie)

# Upload a document to SharePoint
file_path = "/path/to/your/document.docx"
destination_folder = "Shared Documents"  # Specify the destination folder in SharePoint
file_name = "document.docx"  # Specify the name of the file in SharePoint

with open(file_path, "rb") as file:
    site.UploadFile(file, destination_folder, file_name)

# Get the URL of the uploaded document
file_url = site.GetUrl(file_name, destination_folder)
print("Document URL:", file_url)