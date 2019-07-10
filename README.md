
# Python Movie Manager
The purpose of this program is to manage movie downloading. 
You can run the script to either download a single movie or download multiple from a *.txt* or *.csv* file.
## Dependencies
1. Aria2c [latest github release](https://github.com/aria2/aria2/tree/release-1.34.0)
         - command line torrent downloader
  2. Python 3.7 [download page](https://www.python.org/downloads/) 
  3. Pip [installation page](https://pip.pypa.io/en/stable/installing/)
  4. BeautifulSoup [pip installation page](https://pypi.org/project/beautifulsoup4/)
  5. Requests [pip installation page](https://pypi.org/project/requests/)
 
 # Downloading the Program
 1. Clone the repository `git clone https://github.com/lgarceau768/python-movie-download.git`
 2. Modify the `output location` in *config.ini* to output to your desired directory
 # Running the Program
 1. Run the script *"in cmd or powershell"* `.\runProgram.bat` with the desired arguements:
 # Arguements
1. Operation <single/bulk> depending on what you would like to do
2. File/Movie Name
	a. name of the movie if the operation is single
	b. name of the file *".txt" or ".csv"* if the operation is bulk
3. Output location path (full path)
__*example*__
`./runProgram.bat bulk newMovies.csv 'D:\Movies\'`
# Modifying the Program
1. My program uses a txt file for its video extensions, currently I have just been seeing mkv and mp4 files. Add any other extensions to this file with a new line
example:
__*movieExtensions.txt*__

   ` .mp4`
   
   ` .mkv`
   
   ` .avi` -- added extension
   
2. Changing the output location. Currently in the *config.ini* the program is outputting to my network drive. Change this to your specified output
example:
__*config.ini*__

	`[Output]`

	`output location = C:\Movies\ `

# Importing From Csv
Currently I am reading from a csv with this format:

`rank,listed_at,type,title,year,trakt_id,imdb_id,tmdb_id,tvdb_id,url,released,runtime,season_number,season_trakt_id,season_tmdb_id,season_tvdb_id,episode_number,episode_title,episode_released,episode_trakt_id,episode_imdb_id,episode_tmdb_id,episode_tvdb_id,genres`
 (*will soon add support for tv shows*)
 
example:
__*traktList.csv*__ 
    [Pastebin Link](https://pastebin.com/12V6yPfP)

I am using [Trakt.tv](https://trakt.tv) to generate these csv files. -- will add custom csv formats later

# Generating Csv from Trakt - need VIP Account
1.  Login to your Trakt.tv Account
2. Go to the Movies section [Movies](https://trakt.tv/movies)
3. Search for the movie you want to add 
4.  Click the add to watchlist icon: [reference](https://pasteboard.co/ImUqLkJ.png)
5.  Repeat Steps 3-4 for X amount of movies
6.  Go to your profile - top right
7.  Click lists
8.  Then watchlist
9.  Then export as csv icon: [reference](https://pasteboard.co/ImUsPub.png)
10. Then just place the csv in the same directory as the program

 


