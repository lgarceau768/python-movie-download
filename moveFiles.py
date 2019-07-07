import os, sys
from pathlib import Path

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
paths = os.listdir('D:\Movies\\')
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
    for file in os.listdir('D:\Movies\\'+dirName+'\\'):
        for extension in movieFileExtensions:
            if file.endswith(extension):
                path = os.path.join('D:\Movies\\'+dirName+'\\', file)
                if os.path.getsize(path) >= 1000000000: # only move files over 1gb                    
                    #print(path)
                    try:
                        os.system('move '+path+' D:\Movies\\')
                        os.system('rmdir /Q /S D:\Movies\\'+dirName)
                    except Exception as e:
                        print('Error moving path: '+str(path)+' must manually move')
                
                
    