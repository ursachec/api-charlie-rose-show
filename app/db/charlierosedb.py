import sys
sys.path.append("..")

from app.config.db import DB_CONFIG
from app.parser.parser import CharlieRoseParser

import logging
import mysql.connector
from mysql.connector import errorcode

class CharlieRoseDatabaseKeys:

    DB_COLUMN_SHOW_ID_STRING = "show_id_string";
    DB_COLUMN_SHOW_ID_INT = "show_id_int";
    DB_COLUMN_SHOW_URL = "show_url";
    DB_COLUMN_SHOW_VIDEO_CDN_URL = "video_cdn_url";
    DB_COLUMN_SHOW_HAS_ATIPICAL_SOURCE_URL = "has_atipical_source_url";
    DB_COLUMN_SHOW_VIDEO_GOOGLE_SOURCE_URL= "video_google_source_url";
    DB_COLUMN_SHOW_IMAGE_URL= "image_url";

    DB_COLUMN_SHOW_VIDLY_URL = "vidly_url"

    DB_COLUMN_SHOW_HEADLINE = "headline";
    DB_COLUMN_SHOW_GUESTS = "guests";
    DB_COLUMN_SHOW_TOPICS_STRING = "topics_string";

    DB_COLUMN_DATE_PUBLISHED_STRING = "date_published_string";
    DB_COLUMN_DATE_PUBLISHED = "date_published";
    DB_COLUMN_DESCRIPTION = "description";
    DB_COLUMN_KEYWORDS = "keywords";
    DB_COLUMN_COLLECTION = "collections";

    DB_COLUMN_IS_ART_AND_DESIGN = "topics_is_art_and_design";
    DB_COLUMN_IS_BOOKS = "topics_is_books";
    DB_COLUMN_IS_BUSINESS = "topics_is_business";
    DB_COLUMN_IS_CURRENT_AFFAIRS = "topics_is_current_affairs";
    DB_COLUMN_IS_FASHION = "topics_is_fashion";
    DB_COLUMN_IS_FOOD = "topics_is_food";
    DB_COLUMN_IS_HISTORY = "topics_is_history";
    DB_COLUMN_IS_IN_MEMORIAM = "topics_is_in_memoriam";
    DB_COLUMN_IS_LIFESTYLE = "topics_is_lifestyle";
    DB_COLUMN_IS_MOVIES_TV_AND_THEATER = "topics_is_movies_tv_and_theater";
    DB_COLUMN_IS_MUSIC = "topics_is_music";
    DB_COLUMN_IS_RELIGION = "topics_is_religion";
    DB_COLUMN_IS_SCIENCE_AND_HEALTH = "topics_is_science_and_health";
    DB_COLUMN_IS_SPORTS = "topics_is_sports";
    DB_COLUMN_IS_TECHNOLOGY = "topics_is_technology";


topicsMap = {
    "art_design" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_ART_AND_DESIGN ,
    "books" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_BOOKS ,
    "business" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_BUSINESS ,
    "current_affairs" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_CURRENT_AFFAIRS ,
    "fashion" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_FASHION ,
    "food" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_FOOD ,
    "history" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_HISTORY ,
    "in_memoriam" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_IN_MEMORIAM ,
    "lifestyle" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_LIFESTYLE ,
    "movies_tv_theater" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_MOVIES_TV_AND_THEATER ,
    "music" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_MUSIC ,
    "religion" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_RELIGION ,
    "science_health" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_SCIENCE_AND_HEALTH ,
    "sports" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_SPORTS ,
    "technology" : CharlieRoseDatabaseKeys.DB_COLUMN_IS_TECHNOLOGY ,
}

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


class CharlieRoseDatabaseManager:
    def __init__(self):
        print "init data manager"

    def dbConnect(self):
        cnx = None
        try:
            cnx = mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong your username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
        return cnx

    def dbGetLatestShows(self, databaseConnection):
        return []

    def fetchShowsWithCategoryId(self, categoryId):
        shows = []
        shows.append("first show")
        shows.append("second show")
        shows.append("third show")
        return shows

    def fetchShowsForSingleTopic(self, topic, dateForOldestShow=None):
        return None


    def dictionaryRepresentationForFetchedRowEntityShow(self, fetchedRow=None):
        returnDictionary = {}
        returnDictionary["headline"] = fetchedRow["headline"]

        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_HEADLINE] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_HEADLINE]
        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_GUESTS] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_GUESTS]
        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_DATE_PUBLISHED] = str(fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_DATE_PUBLISHED])
        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_KEYWORDS] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_KEYWORDS]
        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_IMAGE_URL] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_IMAGE_URL]
        returnDictionary[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_VIDLY_URL] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_VIDLY_URL]
        
        
        returnDictionary["video_description"] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_DESCRIPTION]
        returnDictionary["topics"] = fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_TOPICS_STRING]
        returnDictionary["show_id_string"] = str(fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_ID_STRING])
        returnDictionary["url"] = "/shows/%s"%(str(returnDictionary["show_id_string"]))
        returnDictionary["id"] = str(fetchedRow[CharlieRoseDatabaseKeys.DB_COLUMN_SHOW_ID_STRING])

        return returnDictionary

    def fetchSingleShowForIdString(self, showIdString):

        showDictionary = {}
        connection = self.dbConnect()
        cursor = connection.cursor(cursor_class=MySQLCursorDict)

        values =  {
            "show_id_int" : int(showIdString)
        }
        query = ("SELECT * FROM charlierose WHERE `show_id_string`=%(show_id_int)s LIMIT 1;")
        cursor.execute(query, values)
        row = cursor.fetchone()
        showDictionary = self.dictionaryRepresentationForFetchedRowEntityShow(row)

        return showDictionary

    def fetchShowsForTopicString(self, topicString, dateForOldestShow=None):
        shows = []

        allowed_topics = ["all", "art_design", "books", "business", "current_affairs", "fashion", "food", "history", "in_memoriam", "lifestyle", "movies_tv_theater", "music", "religion", "science_health", "sports", "technology"];
        if topicString not in allowed_topics:
            return shows

        shouldReturnShowsForAllTopics = (topicString == "all")
        whereClause = ""

        connection = self.dbConnect()
        cursor = connection.cursor(cursor_class=MySQLCursorDict)

        if (shouldReturnShowsForAllTopics):
            query = ("SELECT * FROM charlierose ORDER BY date_published DESC LIMIT 64;")
        else:
            whereClauseCondition = topicsMap[topicString]
            query = "SELECT * FROM charlierose WHERE %s=1 ORDER BY date_published DESC LIMIT 64;"%(whereClauseCondition)

        cursor.execute(query)

        rows = cursor.fetchall()

        print len(rows)

        for r in rows:
            shows.append(self.dictionaryRepresentationForFetchedRowEntityShow(r))

        connection.close()

        return shows

    def fetchShowFromDatabaseWithInfoDictionary(self, infoDictionary):
        show = self.getMockShow()
        show = None
        return show

    def mockHeadlineForId(self, show_id):
        string = 'NO_HEADLINE'

        if str(show_id) == "1234":
            string = 'The Central Park Five'
        elif str(show_id) == "5678":
            string = 'Jeff Bezos, Founder and CEO, Amazon.com'
        else:
            string = 'A discussion about the history and future of books with Tim O\'Reilly, Jane Friedman, Jonathan Safran Foer, Ken Auletta, and David Kastan'

        return string

    def getMockShow(self, show_id):
        mockShow={}
        mockShow["show_id_string"] = str(show_id);
        mockShow["show_id_int"] = int(show_id);
        mockShow["show_url"] = 'http://www.charlierose.com/view/content/12634';
        mockShow["video_source_url"] = 'http://charlierose.http.internapcdn.net/charlierose/digitalgrill_content/110212_3.flv';
        mockShow["has_atipical_source_ur"] = 0;
        mockShow["headline"] = self.mockHeadlineForId(show_id)
        mockShow["guests"] = 'Jane Friedman, Jonathan Safran Foer, Tim O\'Reilly, Ken Auletta, David Kastan';
        mockShow["topics_string"] = 'Technology, Books';
        mockShow["date_published_string"] = '';
        mockShow["date_published"] = '2012-11-23 02:18:08';
        mockShow["description"] = 'A discussion about the history and future of books with Tim O\'Reilly, Jane Friedman, Jonathan Safran Foer, Ken Auletta, and David Kastan';
        mockShow["keywords"] = 'pay walls, digital publishing, Amazon, E-readers, kindle, ipad, online, ereader, internet, e-book';
        mockShow["collections"] = None;
        mockShow["topics_is_art_and_design"] = 0;
        mockShow["topics_is_books"] = 1;
        mockShow["topics_is_business"] = 0;
        mockShow["topics_is_current_affairs"] = 0;
        mockShow["topics_is_history"] = 0;
        mockShow["topics_is_in_memoriam"] = 0;
        mockShow["topics_is_lifestyle"] = 0;
        mockShow["topics_is_movies_tv_and_theater"] = 0;
        mockShow["topics_is_music"] = 0;
        mockShow["topics_is_science_and_health"] = 0;
        mockShow["topics_is_sports"] = 0;
        mockShow["topics_is_technology"] = 1;
        mockShow["start_encodings_sent"] = 0;
        mockShow["start_encodings_failed"] = 0;
        mockShow["pending_encodings"] = 0;
        mockShow["finished_encodings"] = 0;
        mockShow["failed_encodings"] = 0;
        mockShow["available"] = 0;
        return mockShow

    def insertToDBClipWithInfoDictionary(self, infoDictionary):
        connection = self.dbConnect()
        self.insertToDBWClipInfoDictionary(connection, infoDictionary)
        connection.close()

    def insertToDBWClipInfoDictionary(self, cnx, clipInfoDictionary):
        c = clipInfoDictionary
        
        showIdString = c[CharlieRoseParser.KEY_SHOW_ID_STRING]
        showIdInt = c[CharlieRoseParser.KEY_SHOW_ID_INT]
        showUrl = c[CharlieRoseParser.KEY_CLIP_URL]
        showVideoCdnUrl = c[CharlieRoseParser.KEY_VIDEO_CDN_URL]
        showHasAtipicalSourceUrl = c[CharlieRoseParser.KEY_HAS_ATIPICAL_SOURCE_URL]
        showVideoGoogleUrl = c[CharlieRoseParser.KEY_VIDEO_GOOGLE_SOURCE_URL]
        showImageUrl = c[CharlieRoseParser.KEY_IMAGE_URL]
        showHeadline = c[CharlieRoseParser.KEY_HEADLINE]
        showGuests = c[CharlieRoseParser.KEY_GUESTS]
        showTopicsString = c[CharlieRoseParser.KEY_TOPICS]
        showDatePublishedString = c[CharlieRoseParser.KEY_DATE_STRING]
        showDatePublished = c[CharlieRoseParser.KEY_DATE]
        showDescription = c[CharlieRoseParser.KEY_DESCRIPTION]
        showKeywords = c[CharlieRoseParser.KEY_KEYWORDS]
        showCollections = c[CharlieRoseParser.KEY_COLLECTIONS]
        showTopicsIsArtAndDesign = c[CharlieRoseParser.KEY_TOPIC_IS_ART_AND_DESIGN]
        showTopicsIsBooks = c[CharlieRoseParser.KEY_TOPIC_IS_BOOKS]
        showTopicsIsBusiness = c[CharlieRoseParser.KEY_TOPIC_IS_BUSINESS]
        showTopicsIsCurrentAffairs = c[CharlieRoseParser.KEY_TOPIC_IS_CURRENT_AFFAIRS]
        showTopicsIsFashion = c[CharlieRoseParser.KEY_TOPIC_IS_FASHION]
        showTopicsIsFood = c[CharlieRoseParser.KEY_TOPIC_IS_FOOD]
        showTopicsIsHistory = c[CharlieRoseParser.KEY_TOPIC_IS_HISTORY]
        showTopicsIsInMemoriam = c[CharlieRoseParser.KEY_TOPIC_IS_IN_MEMORIAM]
        showTopicsIsLifestyle = c[CharlieRoseParser.KEY_TOPIC_IS_LIFESTYLE]
        showTopicsIsMoviesTVAndTheater = c[CharlieRoseParser.KEY_TOPIC_IS_MOVIES_TV_AND_THEATER]
        showTopicsIsMusic = c[CharlieRoseParser.KEY_TOPIC_IS_ART_AND_DESIGN]
        showTopicsIsScienceAndHealth = c[CharlieRoseParser.KEY_TOPIC_IS_SCIENCE_AND_HEALTH]
        showTopicsIsSports = c[CharlieRoseParser.KEY_TOPIC_IS_SPORTS]
        showTopicsIsMusic = c[CharlieRoseParser.KEY_TOPIC_IS_MUSIC]
        showTopicsIsReligion = c[CharlieRoseParser.KEY_TOPIC_IS_RELIGION]
        showTopicsIsTechnology = c[CharlieRoseParser.KEY_TOPIC_IS_TECHNOLOGY]
        showStartEncodingsSent = 0
        showStartEncodingsFailed = 0
        showPendingEncodings = 0
        showFinishedEncodings = 0
        showFailedEncodings = 0
        showIsAvailable = True
        
        add_test_values = { 
            "show_id_string":showIdString,
            "show_id_int":showIdInt,
            "show_url":showUrl,
            "video_cdn_url":showVideoCdnUrl,
            "has_atipical_source_url":showHasAtipicalSourceUrl,
            "video_google_source_url":showVideoGoogleUrl,
            "image_url":showImageUrl,
            "headline":showHeadline,
            "guests":showGuests,
            "topics_string":showTopicsString,
            "date_published_string":showDatePublishedString,
            "date_published":showDatePublished,
            "description":showDescription,
            "keywords":showKeywords,
            "collections":showCollections,
            "topics_is_art_and_design":showTopicsIsArtAndDesign,
            "topics_is_books":showTopicsIsBooks,
            "topics_is_business":showTopicsIsBusiness,
            "topics_is_current_affairs":showTopicsIsCurrentAffairs,
            "topics_is_history":showTopicsIsHistory,
            "topics_is_in_memoriam":showTopicsIsInMemoriam,
            "topics_is_lifestyle":showTopicsIsLifestyle,
            "topics_is_movies_tv_and_theater":showTopicsIsMoviesTVAndTheater,
            "topics_is_music":showTopicsIsMusic,
            "topics_is_science_and_health":showTopicsIsScienceAndHealth,
            "topics_is_sports":showTopicsIsSports,
            "topics_is_technology":showTopicsIsTechnology,
            "start_encodings_sent":showStartEncodingsSent,
            "start_encodings_failed":showStartEncodingsFailed,
            "pending_encodings":showPendingEncodings,
            "finished_encodings":showFinishedEncodings,
            "failed_encodings":showFailedEncodings,
            "available":showIsAvailable
        }

        add_test_query = ("INSERT IGNORE INTO `charlierose` ( `show_id_string`, `show_id_int`, `show_url`, `video_cdn_url`, `has_atipical_source_url`, `video_google_source_url`, `image_url`, `headline`, `guests`, `topics_string`, `date_published_string`, `date_published`, `description`, `keywords`, `collections`, `topics_is_art_and_design`, `topics_is_books`, `topics_is_business`, `topics_is_current_affairs`, `topics_is_history`, `topics_is_in_memoriam`, `topics_is_lifestyle`, `topics_is_movies_tv_and_theater`, `topics_is_music`, `topics_is_science_and_health`, `topics_is_sports`, `topics_is_technology`, `start_encodings_sent`, `start_encodings_failed`, `pending_encodings`, `finished_encodings`, `failed_encodings`, `available`) "
"VALUES ( %(show_id_string)s , %(show_id_int)s, %(show_url)s, %(video_cdn_url)s, %(has_atipical_source_url)s, %(video_google_source_url)s, %(image_url)s, %(headline)s, %(guests)s, %(topics_string)s, %(date_published_string)s, %(date_published)s, %(description)s,  %(keywords)s, %(collections)s, %(topics_is_art_and_design)s, %(topics_is_books)s, %(topics_is_business)s, %(topics_is_current_affairs)s, %(topics_is_history)s, %(topics_is_in_memoriam)s, %(topics_is_lifestyle)s, %(topics_is_movies_tv_and_theater)s, %(topics_is_music)s, %(topics_is_science_and_health)s, %(topics_is_sports)s, %(topics_is_technology)s, %(start_encodings_sent)s, %(start_encodings_failed)s, %(pending_encodings)s, %(finished_encodings)s, %(failed_encodings)s, %(available)s ); ")
        
        print add_test_values

        cursor = cnx.cursor()
        cursor.execute(add_test_query, add_test_values)

        cnx.commit()
        cnx.close()
