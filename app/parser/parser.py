import sys
import re
import html5lib
import logging
from bs4 import BeautifulSoup

from datetime import datetime


class CharlieRoseParser:

    VALUE_NO_DESCRIPTION = "NO_DESCRIPTION"
    VALUE_NO_GUESTS = "NO_GUESTS"


    KEY_SHOW_ID_STRING = "show_id_string"
    KEY_SHOW_ID_INT = "show_id_int"

    KEY_CLIP_URL = "clip_url"
    KEY_HEADLINE = "headline"
    KEY_GUESTS = "guests"
    KEY_TOPICS = "topics"
    KEY_DATE_STRING = "date_published_string"
    KEY_DATE = "date_published"
    KEY_DESCRIPTION = "description"
    KEY_KEYWORDS = "keywords"
    KEY_VIDEOLINK = "video_link"
    KEY_IMAGE_URL = "image_url"

    KEY_COLLECTIONS = "collections"
    KEY_HAS_ATIPICAL_SOURCE_URL = "has_atipical_source_url"
    KEY_VIDEO_CDN_URL = "video_cdn_url"
    KEY_VIDEO_GOOGLE_SOURCE_URL = "video_google_source_url"

    KEY_TOPIC_IS_ART_AND_DESIGN = "Art & Design"
    KEY_TOPIC_IS_BOOKS = "Books"
    KEY_TOPIC_IS_BUSINESS = "Business"
    KEY_TOPIC_IS_CURRENT_AFFAIRS = "Current Affairs"
    KEY_TOPIC_IS_FASHION = "Fashion"
    KEY_TOPIC_IS_FOOD = "Food"
    KEY_TOPIC_IS_HISTORY = "History"
    KEY_TOPIC_IS_IN_MEMORIAM = "In Memoriam"
    KEY_TOPIC_IS_LIFESTYLE = "Lifestyle"
    KEY_TOPIC_IS_MOVIES_TV_AND_THEATER = "Movies, TV & Theater"
    KEY_TOPIC_IS_MUSIC = "Music"
    KEY_TOPIC_IS_RELIGION = "Religion"
    KEY_TOPIC_IS_SCIENCE_AND_HEALTH = "Science & Health"
    KEY_TOPIC_IS_SPORTS = "Sports"
    KEY_TOPIC_IS_TECHNOLOGY = "Technology"

    def __init__(self, aSoup):
        self.soup = aSoup

    def strippedStringValueForTag(self, tag):
        return unicode(tag.string.strip(' \t\n\r'))

    def tagForGuestsAndTopicsAndDate(self, soup):
        guestsAndTopicsAndDate = soup.find_all(id='headline')[0]
        return guestsAndTopicsAndDate.p

    def tagForHeadline(self, soup):
        headline = soup.find_all(id='headline')[0]
        return headline.h2.span

    def valueForHeadline(self, soup, prettifiedSoup):
        headlineTag = self.tagForHeadline(soup)
        return self.strippedStringValueForTag(headlineTag)

    def valueForGuests(self, soup, prettifiedSoup):
        guests = []
        guestsAndTopicsAndDateTag = self.tagForGuestsAndTopicsAndDate(soup)
        guestAnchors = guestsAndTopicsAndDateTag.find_all("a",href=re.compile("guest"))
        for anchor in guestAnchors:
            guests.append(anchor.string)
        return "with "+", ".join(guests)

    def valueForTopics(self, soup, prettifiedSoup):
        topics = []
        guestsAndTopicsAndDateTag = self.tagForGuestsAndTopicsAndDate(soup)
        topicAnchors = guestsAndTopicsAndDateTag.find_all("a",href=re.compile("topic"))
        for anchor in topicAnchors:
            topics.append(anchor.string)
        return ", ".join(topics)

    def valueForDate(self, soup, prettifiedSoup):
        dateString = self.valueForDateString(soup, prettifiedSoup)
        date_object = datetime.strptime(dateString, 'on %A, %B %d, %Y')
        return date_object

    def valueForDateString(self, soup, prettifiedSoup):
        guestsAndTopicsAndDateTag = self.tagForGuestsAndTopicsAndDate(soup)
        dateString = ""
        for child in guestsAndTopicsAndDateTag.children:
            if type(child).__name__=="Tag":
                continue;
            elif "on " in child:
                dateString = child
        return dateString.strip(' \t\n\r')

    def tagForDescription(self, soup):
        description = soup.find_all(class_='video-description')[0]
        return description.dd.p

    def valueForDescription(self, soup, prettifiedSoup):
        descriptionTag = self.tagForDescription(soup)
        if descriptionTag.string == None:
            return "NO_DESCRIPTION"
        return self.strippedStringValueForTag(descriptionTag)

    def tagForKeywords(self, soup):
        keywordsTag = soup.find_all(class_='video-keywords')[0]
        return keywordsTag

    def valueForKeywords(self, soup, prettifiedSoup):
        keywordsTag = self.tagForKeywords(soup)
        keywordsList = []
        for tag in keywordsTag.find_all("dd"):
            tagValue = tag.a.string
            if tagValue:
                keywordsList.append(tag.a.string)
        if len(keywordsList)>0:
            return ", ".join(keywordsList)
        else:
            return "NO_KEYWORDS_FOUND"

    def testValueForUnconvertedViewLink(self, soup, prettifiedSoup):
        stringCdn = "\nclip: {\n\"url\":\"http://charlierose.http.internapcdn.net/charlierose/digitalgrill_content/alejandropoireGR.flv\" \n},\n"
        stringGoogle = "\n\n<html>\n<link rel=\"video_src\" href=\"http://www.charlierose.com/swf/CRGoogleVideo.swf?docId=-8170799541354106652%3A0%3A43000\" />" 
        matchCdn = self.valueForUnconvertedViewLink(soup, prettifiedSoup)
        matchGoogle = self.valueForUnconvertedViewLink(soup, prettifiedSoup)
        expectedResultCdn = "abc"
        expectedResultGoogle = "abc"
        didMatchCdn = (matchCdn == expectedResultCdn)
        didMatchGoogle = (matchGoogle == expectedResultGoogle)
        return (didMatchCdn and didMatchGoogle)

    def valueForUnconvertedViewLinkGoogle(self, soup, prettifiedSoup):
        foundGoogleLink = None
        m = re.search(r"(^\s*<link\s*href=\"([^\"]+)\"(?=\s+rel=\"video_src\"))", prettifiedSoup, re.MULTILINE)
        if m:
            foundGoogleLink = m.group(2)

        n = re.search(r"(^\s*<link\s+rel=\"video_src\"\s+href=\"([^\"]+)\")", prettifiedSoup, re.MULTILINE)
        if n:
            foundGoogleLink = m.group(2)

        return foundGoogleLink

    def valueForUnconvertedViewLinkCDN(self, soup, prettifiedSoup):
        foundCDNLink = None
        m = re.search(r"(\"url\":\"([^\"]+)\")", prettifiedSoup, re.MULTILINE)
        if m:
            foundCDNLink = m.group(2)

        return foundCDNLink

    def valueForUnconvertedViewLink(self, soup, prettifiedSoup):
        foundLink = "NO_CLIP_URL_FOUND"

        # try to find google video
        foundLink = self.valueForUnconvertedViewLinkGoogle(soup, prettifiedSoup)

        # try to find cdn video
        if foundLink == None:
            foundLink = self.valueForUnconvertedViewLinkCDN(soup, prettifiedSoup)

        return foundLink

    def testValueForClipUrl(self, soup, prettifiedSoup):
        string = "\n\naaaa\n\nclip_url = \'http://www.charlierose.com/view/content/12656\';\n\nsfdsfdsfs\n\nasda"
        match = self.valueForClipUrl(soup)
        return match == "http://www.charlierose.com/view/content/12656"

    def valueForClipUrl(self, soup, prettifiedSoup):
        m = re.search(r"(^\s*\w+_\w+\s*=\s*[\'](\w+[^\']+)\')", prettifiedSoup, re.MULTILINE)
        if m:
            return m.group(2)
        else:
            return "NO_CLIP_URL_FOUND"

    def valueForTopicIsArtAndDesign(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return False
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_ART_AND_DESIGN))

    def valueForTopicIsBooks(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_BOOKS))

    def valueForTopicIsBusiness(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_BUSINESS))

    def valueForTopicIsCurrentAffairs(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_CURRENT_AFFAIRS))

    def valueForTopicIsFashion(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_FASHION))

    def valueForTopicIsFood(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_FOOD))

    def valueForTopicIsHistory(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_HISTORY))

    def valueForTopicIsInMemoriam(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_IN_MEMORIAM))

    def valueForTopicIsLifestyle(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_LIFESTYLE))

    def valueForTopicIsMoviesTVAndTheater(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_MOVIES_TV_AND_THEATER))

    def valueForTopicIsMusic(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_MUSIC))

    def valueForTopicIsReligion(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_RELIGION))

    def valueForTopicIsScienceAndHealth(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_SCIENCE_AND_HEALTH))

    def valueForTopicIsSports(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_SPORTS))
    
    def valueForTopicIsTechnology(self, infoDictionary):
        topicsString = str(infoDictionary[self.KEY_TOPICS])
        return (-1 != topicsString.find(self.KEY_TOPIC_IS_TECHNOLOGY))

    def valueForCollections(self, soup, prettifiedSoup):
        return "NO_COLLECTIONS_SEARCHED_FOR"

    def valuerForHasAtipicalSourceUrl(self, soup, prettifiedSoup):
        return (None != self.valueForUnconvertedViewLinkGoogle(soup, prettifiedSoup))

    def valuerForShowIdString(self, soup, prettifiedSoup):
        showIdString = "0"
        clipUrl = self.valueForClipUrl(soup, prettifiedSoup)
        m = re.search(r"(/(\d+))", clipUrl, re.MULTILINE)
        if m:
            showIdString = m.group(2)
        return showIdString

    def valuerForShowIdInt(self, soup, prettifiedSoup):
        return int(self.valuerForShowIdString(soup, prettifiedSoup))
    
    def valueForImageLink(self, soup, prettifiedSoup):
            foundImageLink = None
            m = re.search(r"(^\s*<link\s*href=\"([^\"]+)\"(?=\s+rel=\"image_src\"))", prettifiedSoup, re.MULTILINE)
            if m:
                foundImageLink = m.group(2)

            n = re.search(r"(^\s*<link\s+rel=\"image_src\"\s+href=\"([^\"]+)\")", prettifiedSoup, re.MULTILINE)
            if n:
                foundImageLink = m.group(2)

            return foundImageLink

    def showInfoDictionaryForSoup(self, soup):
        prettifiedSoup = soup.prettify()
        i = {}
        
        i[self.KEY_SHOW_ID_STRING] = self.valuerForShowIdString(soup, prettifiedSoup)
        i[self.KEY_SHOW_ID_INT] = self.valuerForShowIdInt(soup, prettifiedSoup)

        i[self.KEY_CLIP_URL] = self.valueForClipUrl(soup, prettifiedSoup)
        i[self.KEY_HEADLINE] = self.valueForHeadline(soup, prettifiedSoup)
        i[self.KEY_GUESTS] = self.valueForGuests(soup, prettifiedSoup)
        i[self.KEY_TOPICS] = self.valueForTopics(soup, prettifiedSoup)
        i[self.KEY_DATE] = self.valueForDate(soup, prettifiedSoup)
        i[self.KEY_DATE_STRING] = self.valueForDateString(soup, prettifiedSoup)
        

        i[self.KEY_DESCRIPTION] = self.valueForDescription(soup, prettifiedSoup)
        i[self.KEY_KEYWORDS] = self.valueForKeywords(soup, prettifiedSoup)
        i[self.KEY_VIDEOLINK] = self.valueForUnconvertedViewLink(soup, prettifiedSoup)
        
        i[self.KEY_IMAGE_URL] = self.valueForImageLink(soup, prettifiedSoup)
        

        i[self.KEY_COLLECTIONS] = self.valueForCollections(soup, prettifiedSoup)
        i[self.KEY_HAS_ATIPICAL_SOURCE_URL] = self.valuerForHasAtipicalSourceUrl(soup, prettifiedSoup)
        i[self.KEY_VIDEO_CDN_URL] = self.valueForUnconvertedViewLinkCDN(soup, prettifiedSoup)
        i[self.KEY_VIDEO_GOOGLE_SOURCE_URL] = self.valueForUnconvertedViewLinkGoogle(soup, prettifiedSoup)

        i[self.KEY_TOPIC_IS_ART_AND_DESIGN] = self.valueForTopicIsArtAndDesign(i)
        i[self.KEY_TOPIC_IS_BOOKS] = self.valueForTopicIsBooks(i)
        i[self.KEY_TOPIC_IS_BUSINESS] = self.valueForTopicIsBusiness(i)
        i[self.KEY_TOPIC_IS_CURRENT_AFFAIRS] = self.valueForTopicIsCurrentAffairs(i)
        i[self.KEY_TOPIC_IS_FASHION] = self.valueForTopicIsFashion(i)
        i[self.KEY_TOPIC_IS_FOOD] = self.valueForTopicIsFood(i)
        i[self.KEY_TOPIC_IS_HISTORY] = self.valueForTopicIsHistory(i)
        i[self.KEY_TOPIC_IS_IN_MEMORIAM] = self.valueForTopicIsInMemoriam(i)
        i[self.KEY_TOPIC_IS_LIFESTYLE] = self.valueForTopicIsLifestyle(i)
        i[self.KEY_TOPIC_IS_MOVIES_TV_AND_THEATER] = self.valueForTopicIsMoviesTVAndTheater(i)
        i[self.KEY_TOPIC_IS_MUSIC] = self.valueForTopicIsMusic(i)
        i[self.KEY_TOPIC_IS_RELIGION] = self.valueForTopicIsReligion(i)
        i[self.KEY_TOPIC_IS_SCIENCE_AND_HEALTH] = self.valueForTopicIsScienceAndHealth(i)
        i[self.KEY_TOPIC_IS_SPORTS] = self.valueForTopicIsSports(i)
        i[self.KEY_TOPIC_IS_TECHNOLOGY] = self.valueForTopicIsTechnology(i)

        return i
        
        

    def prettyPrintClipInfoDictionary(self, clipInfoDictionary):
        clipUrlValue = clipInfoDictionary[self.KEY_CLIP_URL]
        headlineValue = clipInfoDictionary[self.KEY_HEADLINE]
        guestsValue = clipInfoDictionary[self.KEY_GUESTS]
        topicsValue = clipInfoDictionary[self.KEY_TOPICS]
        dateValue = clipInfoDictionary[self.KEY_DATE]
        descriptionValue = clipInfoDictionary[self.KEY_DESCRIPTION]
        keywordsValue = clipInfoDictionary[self.KEY_KEYWORDS]
        unconvertedVideoLinkValue = clipInfoDictionary[self.KEY_VIDEOLINK]


        print "ClipUrl: " + clipUrlValue
        print "Headline: " + headlineValue
        print "Guests: " + guestsValue
        print "Topics: " + topicsValue
        print "Date: " + dateValue
        print "Description: " + descriptionValue
        print "Keywords: " + keywordsValue
        print "Video link: " + unconvertedVideoLinkValue