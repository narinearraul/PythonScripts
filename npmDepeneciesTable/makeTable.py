# This script will take your package.json file for your node dependencies and
# make a markdown file with a table with their details
# 3/17/16
import json
import itertools
from bs4 import BeautifulSoup
import requests

modules = open("package.json", "r")
packageJson = modules.read()

print "########################\n"
print "Package.json file you provided is: %s" % packageJson
print "########################\n"
packageJson = json.loads(packageJson)
dependencies = packageJson["dependencies"]
devDependencies = packageJson["devDependencies"]

    
def scrapeData(module):
    url = "https://www.npmjs.com/package/" + module
    #print module name in the md file followd by a pipe
    print  "| " + module + " | ",
    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data, "html.parser")
    infoBox = soup.find("ul", class_="box")
    for span in infoBox.find_all("span"):
        print ' '.join(span.text.split()),
        print " | " ,
    for version in infoBox.find_all("strong"):
        print version.text + " | ",
    count = 0
    for links in infoBox.find_all("a"):
        if count != 0:
            print "[" + links.text + "](" + links.get('href') + ") | ",
        count += 1
        
#start a md file and write the table headers
print "| Module Name | Publisher | Date Published | Version | GitHub | License |"
print "|:------------| ----------| ---------------| --------| -------| -------:|"

# print dependencies
for key in itertools.chain(dependencies,devDependencies):
    scrapeData(key)
    print " "
    