import os, sys, configparser, urllib.request, sys
from bs4 import BeautifulSoup

# defined functions
def checkExists(filename):
    cwd = os.getcwd()
    fileLocation = cwd + filename
    if not os.path.isfile(fileLocation):
        with open(filename, 'w') as file:
            file.close()
    

# import the config file
config = configparser.ConfigParser()
config.read('config.ini')\

# pull the name of the movie from the command line
#movieName = sys.argv[1]

# determine the year of the movie release
#
#
#

# debug url will change to loop after
url = 'http://sv4avadl.uploadt.com/Movie/2017/'

# set up the user agent and opening the Url
req = urllib.request.Request(url, headers={'User-Agent':'Morzilla/5.0'})
c = urllib.request.urlopen(req).read()

# parsing the content of the url
soup = BeautifulSoup(c, 'html.parser') # change to lxml for linux devices

# interating through all links
linkList = []
for link in soup.find_all('a', href=True):
    # skip the line to go to the parent directory
    if link['href'] == '../' or link['href'] =='Parent Directory': 
        continue
    
    else: # extract link if it is a file
        linkList.append(urllib.parse.urljoin(url, link['href'])+'\n')
        continue

# pull a given movie down

## need to format the list into a list of f arrays [name,location]



# # write links to file
# checkExists('links.txt')
# with open('links.txt','w') as linkFile:
#     for link in linkList:
#         linkFile.write(link)