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

# function to return already downloaded movies
def getMovies():
    movieList = []
    if not os.path.isfile('listOfMovies.txt'):
        return None
    else:
        movieList = readFile('listOfMovies.txt')
        newList = []
        for movie in movieList:
            newList.append(movie.replace('.',' '))
    movieList = newList
    return movieList   

# check to see if the movie is already downloaded
def checkDownloaded(movie, downloadedList):
    if downloadedList is not None:
        for dlMovie in downloadedList:
            if dlMovie is not None:
                dlMovie = dlMovie.strip()
                movie = movie.strip()
                if movie in dlMovie:
                    return True
    return False

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
    #print(movieName)
    downloadedMovies = getMovies()
    if not checkDownloaded(movieName, downloadedMovies):
        os.system("python auto-py-torrent.py 1 1 '"+movieName.replace(' ','_')+"'")
    else:
        print('Movie already downloaded')
if operation == 'bulk':
    movies = readFile(fileName)
    downloadedMovies = getMovies()
    #@print(movies)
    with open('movieMagnets.txt', 'w') as file:
        file.close()
    for movie in movies:
        
        if not checkDownloaded(movie, downloadedMovies):
        #print('movie')
            os.system('python .\\auto-py-torrent.py 1 1 '+movie.replace(' ','_'))
        else:
            print('Movie already downloaded')

# now output the movies to a text file

# find the total runtime of the program
print(sys.argv[0][2:]+' took %s seconds' % (time.time() - startTime))
            