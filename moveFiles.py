import os, sys, configparser, shutil

# function to get movie extensions from file
def getMovieExtensions():
    if not os.path.isfile('movieExtensions.txt'):
        with open('movieExtensions.txt', 'w') as extFile:
            extFile.close()
    extList = []
    with open('movieExtensions.txt','r') as extFile:
        lines = extFile.readlines()
        for line in lines:
            if len(line) >= 1:
                extList.append(line.strip())
    return extList

# function to get dir names
def getDirNames(pathList, extensions):
    dirNames = []
    for path in pathList:
        movie = False
        for ext in movieFileExtensions:
            if ext in path:
                movie = True
        if not movie:
            dirNames.append(path)
    return dirNames

# get subdirs
config = configparser.ConfigParser()
config.read('config.ini')
outputDir = config.get('Output', 'output location')
paths = os.listdir(outputDir)
movieFileExtensions = getMovieExtensions()
dirNames = getDirNames(paths, movieFileExtensions)
newList = []
for dirName in dirNames:
    if 'DS_Store' not in dirName:
        if '.ts' not in dirName:
            if '.txt' not in dirName:
                newList.append(dirName)
dirNames = newList

for dirName in dirNames:
    for file in os.listdir(outputDir+dirName+'\\'):
        #print('dirName: '+dirName+' file '+file)
        for extension in movieFileExtensions:
            #print('extension: '+extension)
            if file.endswith(extension):
                path = os.path.join(outputDir+'\\'+dirName+'\\'+file)
                dirPath = os.path.join(outputDir+'\\'+dirName)
                if not os.path.isfile('listOfMovies.txt'):
                    with open('listOfMovies.txt', 'w') as file:
                        file.close()
                with open('listOfMovies.txt', 'a') as movieList:
                    movieList.write(os.path.join(file)+'\n')
                #os.system('move '+path+' \''+outputDir+'\'') 
                try:
               	    shutil.move(path, outputDir)
                    shutil.rmtree(dirPath)
		except Exception as e:
		    print('Exception in moving / deleting files %s' % str(e))

                   
    