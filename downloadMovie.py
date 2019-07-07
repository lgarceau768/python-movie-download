import os, sys, configparser, urllib.request, sys, re, requests, time, csv
from bs4 import BeautifulSoup

#### defined functions

# check to see if a file exists
def checkExists(filename):
    cwd = os.getcwd()
    #fileLocation = cwd + filename 
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            file.close()



# function to read the sources from the text file
def readFile(file):
    fileList = []
    checkExists(file)
    if file.endswith('.txt'):
        with open(file, 'r') as sourceFile:
            read = sourceFile.readlines()
            for line in read:
                if len(line) > 2:
                    fileList.append(line.strip())
    elif file.endswith('.csv'):
        with open(file, 'r') as traktFile:
            csvReader = csv.reader(traktFile, delimiter=',')
            lineCount = 0
            for row in csvReader:
                if lineCount == 0:
                    # column names
                    lineCount += 1
                else:
                    movieName = row[3]
                    if movieName is not None:
                        if len(movieName) > 1:
                            fileList.append(movieName)
    return fileList
            

####  main script
# find the total time execution of the program
startTime = time.time()

print(str(sys.argv))

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
found = False
movieList = []

if operation == 'single':
    # run the auto-py-torrent script options 0 1 moviename
    print(movieName)
    os.system("python auto-py-torrent.py 1 1 '"+movieName.replace(' ','_')+"'")
if operation == 'bulk':
    movies = readFile(fileName)
    print(movies)
    for movie in movies:
        #print('movie')
        os.system('python .\\auto-py-torrent.py 1 1 '+movie.replace(' ','_'))

# now output the movies to a text file

# find the total runtime of the program
print(sys.argv[0][2:]+' took %s seconds' % (time.time() - startTime))
            