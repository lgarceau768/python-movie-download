import os, sys, configparser, urllib.request, sys, re, requests, time
from bs4 import BeautifulSoup

# read variables from config file
config = configparser.ConfigParser()
config.read('config.ini')

sourceFile = config.read('Settings', 'source file')
outputFile = config.read('Settings', 'output file')

#### defined functions
# check to see if a file exists
def checkExists(filename):
    cwd = os.getcwd()
    #fileLocation = cwd + filename 
    if not os.path.isfile(filename):
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
    try:
        c = urllib.request.urlopen(req).read()
    except Exception as e:
        print('Exception in reading url: '+url+' '+str(e))
        return None
    # parsing the content of the url
    soup = BeautifulSoup(c, 'html.parser') # change to lxml for linux devices

    # interating through all links
    linkList = []
    #print('url: '+url)
    for link in soup.find_all('a', href=True):
        # skip the line to go to the parent directory
        #print(link['href'])
        linkList.append(link['href'].replace('%20', ''))
        
    
    return linkList

# function to write file
def writeFile(list, filename):
    checkExists(filename)
    with open(filename, 'w') as linkFile:
        for line in list:
            linkFile.write(line+'\n')
        linkFile.close()

# function to read the sources from the text file
def readFile(file):
    fileList = []
    checkExists(searchFile)
    with open(searchFile, 'r') as sourceFile:
        read = sourceFile.readlines()
        for line in read:
            if len(line) > 2:
                fileList.append(line.strip())
    return fileList

# function to look for a given movie in a given source url
def getMovieUrl(movieName):
    movieNameSearch = movieName.replace(' ','+').lower()
    links = getLinks(source+movieNameSearch)
    for link in links:
        movieNameSearch = movieNameSearch.replace('+','-')
        if movieNameSearch in link:
            return link
                  

####  main script
# find the total time execution of the program
startTime = time.time()

# get operation and moviename
operation = sys.argv[1].lower()
name = sys.argv[2]
movieName = ''
fileName = ''
if operation == 'single':
    movieName = name
elif operation == 'bulk':
    fileName = name
else:
    print('Invalid operation <single/bulk> not: '+operation)
    sys.exit(0)

# get search sources: - <single/bulk>
sourceList = readFile(sourceFile)
found = False
movieList = []
for source in sourceList:
    if operation == 'single':
        movieList.append(getMovieUrl(movieName))
    if operation == 'bulk':
        movies = readFile(fileName)
        for movie in movies:
            movieList.append(getMovieUrl(movie))

# now output the movies to a text file
writeFile(movieList, outputFile)

# find the total runtime of the program
print(sys.argv[0][2:]+' took %s seconds' % (time.time() - startTime))
            