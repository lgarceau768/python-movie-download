@echo off
set /p operation=%1
set /p name=%2

python .\downloadMovie.py %operation% %name%
cd D:\Movies\
for /f "delims=" %%a in (D:\python-movie-download\movieMagnets.txt) DO ( 
    aria2c --seed-time=0 --file-allocation=none --bt-stop-timeout=60 --allow-overwrite=false %%a
)

python D:\python-movie-download\moveFiles.py
