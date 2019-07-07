@echo off
set /p operation=Enter Operation: 
set /p name=Enter Name (movieName/fileName)

python .\downloadMovie.py %operation% %name%
cd D:\Movies\
for /f "delims=" %%a in (D:\python-movie-download\bulkmovieMagnets.txt) DO ( 
    aria2c --seed-time=0 %%a
)
python .\moveFiles.py