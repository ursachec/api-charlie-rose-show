import sys
import re
import os
from datetime import date
from bs4 import BeautifulSoup

from app.parser.parser import CharlieRoseParser
from app.db.charlierosedb import CharlieRoseDatabaseManager

ENABLE_DEBUG_LOGGING = True

dbManager = CharlieRoseDatabaseManager()

def log(message):
	if ENABLE_DEBUG_LOGGING:
		print message

def handleShowsFromDirectory(directory):
    files = os.listdir(directory)
    log("handling files from directory({0:d}): {1}".format(len(files), directory))
    limit = 600
    count = 0
    for f in files:
        currentFilename = directory+"/"+f
        handleShowFromFile(currentFilename)

        if count > limit:
            break
        count += 1

def handleClipInfoDictionary(infoDictionary):
	if infoDictionary:
		dbManager.insertToDBClipWithInfoDictionary(infoDictionary)

def handleShowFromFile(filename):
    log("\nhandling file: {0}".format(filename))
    m = re.search(r"(\.DS)", filename, re.MULTILINE)
    if m:
    	log("\skipping .DS_STORE file: {0}".format(filename))
    	return;

    soup = BeautifulSoup(open(filename), "html5lib")

    # get clip info from soup
    parser = CharlieRoseParser(soup)
    clipInfoDictionary = parser.showInfoDictionaryForSoup(soup)
    handleClipInfoDictionary(clipInfoDictionary)

def prettyPrintClipInfoDictionary(clipInfoDictionary):
        clipUrlValue = clipInfoDictionary[CharlieRoseParser.KEY_CLIP_URL] 
        headlineValue = clipInfoDictionary[CharlieRoseParser.KEY_HEADLINE]
        guestsValue = clipInfoDictionary[CharlieRoseParser.KEY_GUESTS]
        topicsValue = clipInfoDictionary[CharlieRoseParser.KEY_TOPICS]
        dateValue = clipInfoDictionary[CharlieRoseParser.KEY_DATE]
        descriptionValue = clipInfoDictionary[CharlieRoseParser.KEY_DESCRIPTION]
        keywordsValue = clipInfoDictionary[CharlieRoseParser.KEY_KEYWORDS]
        unconvertedVideoLinkValue = clipInfoDictionary[CharlieRoseParser.KEY_VIDEOLINK]

        log("ClipUrl: " + clipUrlValue)
        log("Headline: " + headlineValue)
        log("Guests: " + guestsValue)
        log("Topics: " + topicsValue)
        log("Date: " + dateValue)
        log("Description: " + descriptionValue)
        log("Keywords: " + keywordsValue)
        log("Video link: " + unconvertedVideoLinkValue)

# define directory where to look for shows
# directory = os.environ.get('CR_HTML_FILES_DIRECTORY')
directory = "/Users/claudiu.ursache/code/charlie-rose/new-content/html"
print "handling files from directory: {0}".format(directory)

handleShowsFromDirectory(directory)

