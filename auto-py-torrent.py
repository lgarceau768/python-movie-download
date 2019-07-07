#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""auto_py_torrent.

This module provides utilities to download a torrent within specific types.
"""

# Author: Gabriel Scotillo
# URL: https://github.com/ocslegna/auto_py_torrent
# Please do not download illegal torrents or torrents that you do not have
#     permission to own.
# This tool is for educational purposes only. Any damage you make will not
#     affect the author.


import os
import subprocess
import sys
import traceback
import logging
import argparse
import re
import textwrap
import coloredlogs
import requests
import time

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from tabulate import tabulate


MODES = 'best_rated list'.split()


TORRENTS = ({'torrent_project':
             {'page': 'https://torrentproject.se/?t=',
              'key_search': 'No results',
              'domain': 'https://torrentproject.se'}},
            {'the_pirate_bay':
             {'page': 'https://openpirate.org/search.php?q=',
              'key_search': 'No hits',
              'domain': 'https://openpirate.org'}})
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
coloredlogs.install()


class Colors:
    """Color class container."""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    GREEN = '\033[42m'
    CYAN = '\033[36m'
    RED = '\033[41m'
    PINK = '\033[95m'
    PURPLE = '\033[35m'
    LIGHTBLUE = '\033[94m'
    LGREEN = '\033[0m\033[32m'
    LIGHTCYAN = '\033[0m\033[36m'
    LRED = '\033[0m\033[31m'
    LIGHTPURPLE = '\033[0m\033[35m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


def get_parser():
    """Load parser for command line arguments.

    It parses argv/input into args variable.
    """
        # Parent and only parser.
    parser = argparse.ArgumentParser(
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('mode', action='store',
                        choices=range(len(MODES)),
                        type=int,
                        help='Select mode of file download.\n'
                             '    e.g: 0(rated) or 1(list).')
    parser.add_argument('torr_page', action='store',
                        choices=range(len(TORRENTS)),
                        type=int,
                        help='Select tracking page to download from.\n'
                             '    e.g: 0 to .. ' + str(len(TORRENTS)-1) + '.')
    parser.add_argument('str_search', action='store',
                        type=str,
                        help='Input torrent string to search.\n'
                             '    e.g: "String search"')
    return(parser)


def is_num(var):
    """Check if var string is num. Should use it only with strings."""
    try:
        int(var)
        return True
    except ValueError:
        return False


class AutoPy:
    """AutoPy class for instance variables."""

    def __init__(self, args, string_search, mode_search,
                 page, key_search, torrent_page, domain):
        """Args not entered will be defaulted."""
        self.args = args
        self.back_to_menu = False
        self.content_page = None
        self.domain = domain
        self.elements = None
        self.found_torrents = False
        self.hrefs = []
        self.keep_search = True
        self.key_search = key_search
        self.magnet = ""
        self.mode_search = mode_search
        self.page = page
        self.picked_choice = False
        self.selected = ""
        self.string_search = string_search
        self.table = None
        self.torrent = ""
        self.torrent_page = torrent_page
        self.url = ""
        self.movieName = ""
        self.retries = 0

    
    def get_magnet(self, url):
        """Get magnet from torrent page. Url already got domain."""
        #print(url+ '\ndomain:  '+self.domain)
        if 'magnet' in url:
            url = url.replace(self.domain, '')
        self.url = url
        if not os.path.isfile('movieMagnets.txt'):
            with open('movieMagnets.txt', 'w') as file:
                file.close()
        with open('movieMagnets.txt', 'a') as linkFile:
            linkFile.write(url+'\n')
        

    def download_torrent(self):
        """Download torrent.

        Rated implies download the unique best rated torrent found.
        Otherwise: get the magnet and download it.
        """
        try:
            if self.back_to_menu is True:
                return
            if self.found_torrents is False:
                print('Nothing found.')
                return
            elif self.mode_search == 'list':
                if self.selected is not None:
                    # t_p, pirate and 1337x got magnet inside, else direct.
                    if self.page in ['the_pirate_bay',
                                       'torrent_project',
                                       '1337x',
                                       'isohunt']:
                        url = self.hrefs[int(self.selected)]
                        self.get_magnet(url)
                        print('Downloading movie: '+self.movieName+' from url: '+url)
                    else:
                        print('Bad selected page.')
                else:
                    print('Nothing selected.')
                    sys.exit(1)
        except Exception:
            print(traceback.format_exc())
            sys.exit(0)

    def build_table(self):
        """Build table."""
        headers = ['Title', 'Seeders', 'Leechers', 'Age', 'Size']
        titles = []
        seeders = []
        leechers = []
        ages = []
        sizes = []

        if self.page == 'the_pirate_bay':
            for elem in self.elements[0]:
                title = elem.find('a', {'class': 'detLink'}).get_text()
                titles.append(title)

                font_text = elem.find(
                    'font', {'class': 'detDesc'}).get_text()
                dammit = UnicodeDammit(font_text)
                age, size = dammit.unicode_markup.split(',')[:-1]
                ages.append(age)
                sizes.append(size)
                # Torrent
                href = self.domain + \
                    elem.find('a', title=re.compile('magnet'))['href']
                self.hrefs.append(str(href))

            seeders = [elem.get_text() for elem in self.elements[1]]
            leechers = [elem.get_text() for elem in self.elements[2]]

        
        else:
            print('Error page')

        self.table = [[Colors.BOLD +
                       UnicodeDammit(titles[i][:75].strip(), ["utf-8"]).unicode_markup +
                       Colors.ENDC
                       if (i + 1) % 2 == 0
                       else UnicodeDammit(
                           titles[i][:75].strip()).unicode_markup,
                       Colors.SEEDER + seeders[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LGREEN + seeders[i].strip() + Colors.ENDC,
                       Colors.LEECHER + leechers[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.LRED + leechers[i].strip() + Colors.ENDC,
                       Colors.LIGHTBLUE + ages[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.BLUE + ages[i].strip() + Colors.ENDC,
                       Colors.PINK + sizes[i].strip() + Colors.ENDC
                       if (i + 1) % 2 == 0
                       else Colors.PURPLE + sizes[i].strip() + Colors.ENDC]
                      for i in range(len(self.hrefs))]

    def soupify(self):
        """Get proper torrent/magnet information.

        If search_mode is rated then get torrent/magnet.
        If not, get all the elements to build the table.
        There are different ways for each page.
        """
        soup = BeautifulSoup(self.content_page.content, 'lxml')  
        if self.page == 'the_pirate_bay':
            main = soup.find('table', {'id': 'searchResult'})
            if self.mode_search == 'best_rated':
                rated_url = self.domain + \
                    main.find('a', href=re.compile('torrent'))['href']
                self.get_magnet(rated_url)
            else:
                try:                
                    trs = main.find_all('tr', limit=30)[1:]
                    self.elements = list(
                        zip(*[tr.find_all('td', recursive=False)[1:]
                            for tr in trs]))  # Magnets   
                except:
                    if main is None:
                        print('Failed to get data for movie: '+self.movieName+' retrying attempt '+str(self.retries+1)+' out of 5')
                        self.retries += 1
                        time.sleep(5)
                        if self.retries < 5:
                            self.soupify()

        else:
            print('Cannot soupify current page. Try again.')

    def handle_select(self):
        """Handle user's input in list mode."""
        #self.selected = input('>> ')
        self.selected = '0'
        if self.selected in ['Q', 'q']:
            sys.exit(1)
        elif self.selected in ['B', 'b']:
            self.back_to_menu = True
            return True
        elif is_num(self.selected):
            if 0 <= int(self.selected) <= len(self.hrefs) - 1:
                self.back_to_menu = False
                return True
            else:
                print(Colors.FAIL +
                      'Wrong index. ' +
                      'Please select an appropiate one or other option.' +
                      Colors.ENDC)
                return False
        else:
            print(Colors.FAIL +
                  'Invalid input. ' +
                  'Please select an appropiate one or other option.' +
                  Colors.ENDC)
            return False

    def select_torrent(self):
        """Select torrent.

        First check if specific element/info is obtained in content_page.
        Specify to user if it wants best rated torrent or select one from list.
        If the user wants best rated: Directly obtain magnet/torrent.
        Else: build table with all data and enable the user select the torrent.
        """
        try:
            self.found_torrents = not bool(self.key_search in
                                           self.content_page.text)
            if not self.found_torrents:
                print('-----------------No torrents found.--------------------')
                sys.exit(1)
            self.soupify()
            if self.mode_search == 'list':
                self.build_table()
                
                while not(self.picked_choice):
                    self.picked_choice = self.handle_select()
        except Exception:
            print('ERROR select_torrent: ')
            print('Could not download movie: '+self.movieName)
            logging.error(traceback.format_exc())
            sys.exit(0)

    def build_url(self):
        """Build appropiate encoded URL.

        This implies the same way of searching a torrent as in the page itself.
        """
        url = requests.utils.requote_uri(
            self.torrent_page + self.string_search)
        if self.page == '1337x':
            return(url + '/1/')
        elif self.page == 'limetorrents':
            return(url + '/')
        else:
            return(url)

    def get_content(self):
        """Get content of the page through url."""
        url = self.build_url()
        try:
            self.content_page = requests.get(url)
            if not(self.content_page.status_code == requests.codes.ok):
                self.content_page.raise_for_status()
        except requests.exceptions.RequestException as ex:
            logging.info('A requests exception has ocurred: ' + str(ex))
            logging.error(traceback.format_exc())
            sys.exit(0)


def insert(args):
    """Insert args values into instance variables."""
    string_search = args.str_search
    mode_search = MODES[args.mode]
    page = list(TORRENTS[args.torr_page].keys())[0]
    key_search = TORRENTS[args.torr_page][page]['key_search']
    torrent_page = TORRENTS[args.torr_page][page]['page']
    domain = TORRENTS[args.torr_page][page]['domain']
    return([args, string_search, mode_search, page,
            key_search, torrent_page, domain])


def initialize():
    """Initialize script."""
    #print("Welcome to auto_py_torrent!\n")


def run_it():
    """Search and download torrents until the user says it so."""
    initialize()
    parser = get_parser()
    args = None
    first_parse = True
    while(True):
        if first_parse is True:
            first_parse = False
            args = parser.parse_args()
            
        else:
            # print(textwrap.dedent(
            #     '''\
            #     Search again like in the beginning.
            #       -- You can either choose best rated or list mode.
            #       -- This time, you can insert the search string without double quotes.
            #       Remember the list mode options!
            #         0: torrent project.
            #         1: the pirate bay.
            #         2: 1337x.
            #         3: eztv.
            #         4: limetorrents.
            #         5: isohunt.
            #     '''))
            sys.exit(0)
            print('Or.. if you want to exit just write "' +
                  Colors.LRED + 'Q' + Colors.ENDC + '" or "' +
                  Colors.LRED + 'q' + Colors.ENDC + '".')
            input_parse = input('>> ').replace("'", "").replace('"', '')
            if input_parse in ['Q', 'q']:
                sys.exit(1)

            args = parser.parse_args(input_parse.split(' ', 2))
            
        if args.str_search.strip() == "":
            print('Please insert an appropiate non-empty string.')
        else:
            args.str_search = args.str_search.replace('_',' ').replace("'",'')

            movieName = args.str_search
            #print(args.str_search)
            auto = AutoPy(*insert(args))
            auto.movieName = movieName
            auto.get_content()
            auto.select_torrent()
            auto.download_torrent()


def main():
    """Entry point for app script."""
    try:
        run_it()
    except KeyboardInterrupt:
        print('\nSee you the next time.')
    except Exception:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
