import requests
import os

# Change directory to where the script is located

full_path = os.path.realpath(__file__)
file_path = os.path.dirname(full_path)

os.chdir(file_path)

# Address of pdf file: 

url = 'https://treasury.gov.au/sites/default/files/2020-10/p2020-super_0.pdf' 
response = requests.get(url, stream=True)

with open(file_path + '/metadata.pdf', 'wb') as f:
    f.write(response.content)
