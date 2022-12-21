# IBM Python Project for Data Engineering

import os
import requests
from zipfile import ZipFile


# Download zip file and Save it into the data raw directory
Url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/source.zip"
response = requests.get(Url)

cwd = os.getcwd() # Current Working Directory
print(f"The Current Working Directory is {cwd}")

filePath = os.path.join(cwd, "data/raw", "source.zip")
print(f"The Path that zip file will be saved: {filePath}")

with open(filePath, "wb") as output:
    output.write(response.content)

# Unzipping file
directoryFile = os.path.join(cwd, "data/raw")
with ZipFile(filePath, "r") as zipObject:
    zipObject.extractall(directoryFile)
os.remove(filePath)