import requests
from zipfile import ZipFile
import os
import shutil

NOT_DELETE_DIR = ["saves"]

# GitHub repository URL
repository_name = 'Auth'
addr = f"https://github.com/Hacaric/{repository_name}/archive/refs/heads/main.zip"
url = addr

# Paths
update_zip_path = './.update/version.zip'
extract_path = './.update/update_files/'
old_files_path = './'

# Ensure directories exist
os.makedirs(os.path.dirname(update_zip_path), exist_ok=True)
os.makedirs(extract_path, exist_ok=True)
os.makedirs(old_files_path, exist_ok=True)

# Download the file
print("Downloading update from github...")
response = requests.get(url)
if response.status_code == 200:
    with open(update_zip_path, 'wb') as file:
        file.write(response.content)
    print('File downloaded successfully')
else:
    print('Failed to download file')
    exit(1)

# Unzip the file
print("Trying to unzip...")
try:
    with ZipFile(update_zip_path, 'r') as zObject:
        zObject.extractall(path=extract_path)
    print('Files unzipped successfully')
except Exception as e:
    print(f'Failed to unzip files: {e}')
    exit(1)

#Rename to repository name

try:
    old_folder = extract_path + repository_name + "-main"
    new_folder = extract_path + repository_name
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder) 
    os.rename(old_folder, new_folder)
except Exception as e:
    print(f"Failed renaming directory {extract_path}{old_folder} to {repository_name} error: {e}")
    exit(1)
# Delete the zip file
print("Deleting zip...")
os.remove(update_zip_path)

print("Replacing files...")
new_files = [i for i in os.listdir(extract_path+repository_name+"/") if os.path.isfile(f"{extract_path}{repository_name}/{i}")]
for filename in new_files:
    print(f"Replacing {filename}")
    os.replace(f"{extract_path}{repository_name}/{filename}", old_files_path+filename)

print("Replacing folders...")
new_folders = [i for i in os.listdir(extract_path+repository_name+"/") if not os.path.isfile(f"{extract_path}{repository_name}/{i}")]
for folder_name in new_folders:
    if folder_name in NOT_DELETE_DIR and folder_name in os.listdir(old_files_path):
        continue
    if os.path.exists(old_files_path+folder_name):
        print(f"|---Updating {old_files_path+folder_name}")
        shutil.rmtree(old_files_path+folder_name)
    os.makedirs(old_files_path+folder_name)
    os.rename(extract_path+repository_name+"/"+folder_name, old_files_path+folder_name)

print("Update completed.")
print("Cleaning up...")
try: 
    os.rmdir(extract_path+repository_name)
except Exception as e:
    print(f"Failed cleaning, repository probably contained directory. Error: {e}")
    exit(1)
print("\nUpdated successfully.")