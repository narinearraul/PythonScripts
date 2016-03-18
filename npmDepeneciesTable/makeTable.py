# This script will take your package.json file for your node dependencies and
# make a markdown file with a table with their details
# 3/17/16
import sys
import json
import itertools
from bs4 import BeautifulSoup
import requests

modules = open(sys.argv[1], "r")
packageJson = modules.read()
markdown = open(sys.argv[2], "w")
print "########################\n"
print "Package.json file you provided is: %s" % packageJson
print "########################\n"
dependencies = {}
devDependencies = {}
packageJson = json.loads(packageJson)
if  "dependencies" in packageJson.keys():
    dependencies = packageJson["dependencies"]
if  "devDependencies" in packageJson.keys():
    devDependencies = packageJson["devDependencies"]
    
def scrapeData(module):
    moduleInfo = ""
    url = "https://www.npmjs.com/package/" + module
    #print module name in the md file followd by a pipe
    moduleInfo = "| " + module + " | "
    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data, "html.parser")
    infoBox = soup.find("ul", class_="box")
    for span in infoBox.find_all("span"):
        moduleInfo += ' '.join(span.text.split())
        moduleInfo +=  " | " 
    for version in infoBox.find_all("strong"):
        moduleInfo +=  version.text + " | "
    count = 0
    linkCount = len(infoBox.find_all("a"))
    for links in infoBox.find_all("a"):
        if count == 1 and linkCount == 2:
            moduleInfo += " | " 
        if count != 0:
            moduleInfo +=  "[" + links.text + "](" + links.get('href') + ") | "
        count += 1
    print moduleInfo
    return moduleInfo
        
#start a md file and write the table headers
markdown.write("| Module Name | Publisher | Date Published | Version | GitHub | License |\n")
markdown.write("|:------------| ----------| ---------------| --------| -------| -------:|\n")

# print dependencies
for key in itertools.chain(dependencies,devDependencies):
    print "Making row for module: " + key
    moduleInfo = scrapeData(key)
    markdown.write(moduleInfo + "\n")
    
markdown.close();
    