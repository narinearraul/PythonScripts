#
# 4/13/15
# This Script will clean a cloudant database
# except for the keys specified in the exclude.txt file
# Narine Cholakyan
#

import cloudant
import json

from config import PASSWORD
from config import USERNAME
from config import DBNAME

exclude_list = open("exclude.txt", "r")
exclude_keys = exclude_list.read().splitlines()

print "########################\n"
print "Exclude keys you provided are: %s" % exclude_keys
print "########################\n"

#connect to RA-Perch Cloudant instance
cloudantInstance = cloudant.Account(USERNAME, async=True)

#need access
cloudantInstance.login(USERNAME, PASSWORD).result().raise_for_status()

#connect to database nodered
cloudantDB = cloudantInstance.database(DBNAME)
print "########################\n"
cloudantDBInfo = cloudantDB.get().result().json()
print "nodered DB info: %s" % cloudantDBInfo
print "########################\n"
#docs = cloudantDB.document('ff639d3031f35a3f8ffe3262323e68d5') #test hmmmm
count = 0 
for doc in cloudantDB:
	if(doc['id'] not in exclude_keys):
		rev = doc['value']['rev']
		count += 1
		print "deleting doc %s/%s" % (count,cloudantDBInfo['doc_count'])
		print "document id is: %s" % doc['id']
		print "document revision value is: %s" % rev
		docDB = cloudantDB.document(doc['id'])
		docDB.delete(rev)
		print "deleted successfully"
print "%d documents left in %s" % (int(cloudantDBInfo['doc_count'])-int(count), DBNAME)
