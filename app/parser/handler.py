import sys
import re
import os
import shutil
import logging
import string

from bs4 import BeautifulSoup
from parser import CharlieRoseParser



def handleShowsFromDirectory(directory):
    files = os.listdir(directory)
    print "handling files from directory({0:d}): {1}".format(len(files), directory)
    limit = 10
    count = 0
    for f in files:
        currentFilename = directory+"/"+f
        handleShowFromFile(currentFilename)

        if count > limit:
            break
        count += 1

def handleShowFromFile(filename):
    print "\nhandling file: {0}".format(filename)

    soup = BeautifulSoup(open(filename), "html5lib")

    # get clip info from soup
    parser = CharlieRoseParser(soup)
    clipInfoDictionary = parser.showInfoDictionaryForSoup(soup)
    if clipInfoDictionary:
        parser.prettyPrintClipInfoDictionary(clipInfoDictionary)


# define directory where to look for shows
directory = "/Users/claudiu.ursache/code/charlie-rose/content/crwget/CRWGET/www.charlierose.com/view/clip"
handleShowsFromDirectory(directory)

