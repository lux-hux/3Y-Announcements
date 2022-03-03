import os
import shutil

full_path = os.path.realpath(__file__)
file_path = os.path.dirname(full_path)

import getpass
user = getpass.getuser()
try:
    os.mkdir('/Users/' + user + '/Downloads/Company PDFs')
except OSError as error:
    print(error)    



os.chdir('/Users/' + user + '/Downloads')


# old_file = os.path.join(os.getcwd(), "p2020-super_0.pdf")
# new_file = os.path.join(os.getcwd(), "Super.pdf")

# os.rename(old_file, new_file)

import glob

os.getcwd()
glob.glob('*.pdf')
directory = glob.glob('*.pdf')

for i in directory:
    print('fuck')
    if i.endswith(".pdf"):
         os.rename(i,"super2020202021.pdf")



shutil.move('super2020202021.pdf', 'Company PDFs')