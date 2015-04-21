Delete all but certain IDs on cloudant.

Python Script

1. install pip for python https://pip.pypa.io/en/stable/installing.html
2. install cloudant using pip (pip install cloudant)
3. create exclude.txt listing all the document ids that should not be deleted from the database
4. create settings.py for any username/password or other variables you would need to use
5. make sure the files from 3. and 4. are in the same directory as cleanCloudantDB.py
6. run cleanCloudantDB.py
