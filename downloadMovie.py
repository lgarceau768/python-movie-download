import os, sys, configparser, urllib.request, sys, re
from bs4 import BeautifulSoup

# defined functions
def checkExists(filename):
    cwd = os.getcwd()
    fileLocation = cwd + filename
    if not os.path.isfile(fileLocation):
        with open(filename, 'w') as file:
            file.close()
    

# get the movie name
def findMovieName(link):
    nums = set('0123456789')
    for i in range(0, len(link)):
        if link[i] in nums:
            return link[:i]
    return link

# function to get the links from a url
def getLinks(url):

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
            if '.jpg' not in link['href'] and 'mkv' not in link['href']:
                if '720' in link['href'] or '1080' in link['href']:
                    linkList.append(link['href'].replace('%20', ''))
            continue

    # pull a given movie down

    ## need to format the list into a list of f arrays [name,location]
    for i in range(0, len(linkList)):
        url = urllib.parse.urljoin(url, linkList[i])
        name = linkList[i][:len(link)-4]
        pattern = re.compile('\W')
        name = re.sub(pattern, ' ', name)
        linkList[i] = [name, url]

    # remove duplicates
    newList = []
    added = set()
    for val in linkList:
        name = findMovieName(val[0])
        if not name in added:
            newList.append(val)
            added.add(name)
    linkList = newList

    # write links to file
    # checkExists('links.txt')
    # with open('links.txt','w') as linkFile:
    #     for link in linkList:
    #         linkFile.write(str(link)+'\n')
    return linkList

# check if given move is in url

# import the config file
config = configparser.ConfigParser()
config.read('config.ini')\

# pull the name of the movie from the command line
# command line arguement bulk or single
## format python downloadMovie.py <operation bulk/single> <filename/moviename>
operation = str(sys.argv[1])
movieName = ''
fileName = ''
if operation == 'bulk':
    fileName = str(sys.argv[2])
    cwd = os.getcwd()
    if not os.path.isfile(cwd+fileName):
        print('File name specified not valid: '+str(sys.argv[2]))
        sys.exit(0)
elif operation == 'single':
    movieName = str(sys.argv[2])
else:
    print('Invalid Operation either <bulk/single> not ' +str(operation))
    sys.exit(0)


# determine the year of the movie release
#
#
#
