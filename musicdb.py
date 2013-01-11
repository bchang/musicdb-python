import itunes
import operator
import timeutil
from pymongo import MongoClient

__author__ = 'bchang'

connection = MongoClient('localhost', 27017)
db = connection.musicdb
itunesCollection = db.itunes_collection

LABEL_ROW_TEMPLATE = "{:<30}: {:3d}:{:02d}:{:02d}"

def importItunes():
    xmlFile = '/Users/bchang/Music/iTunes/iTunes Music Library.xml'
    itunes.importItunesXml(xmlFile, itunesCollection)

def printAllTracks():
    for itunesTrackData in itunesCollection.find():
        if itunes.KEY_ARTIST in itunesTrackData:
            artist = itunesTrackData[itunes.KEY_ARTIST]
        else:
            artist = ''
        print itunesTrackData[itunes.KEY_TRACK_ID], itunesTrackData[itunes.KEY_NAME], artist

def __groupItemsByKey__(collection, key):
    grouped = dict()
    for itunesTrackData in collection.find({key : {'$exists':True}}):
        val = itunesTrackData[key]
        if val not in grouped:
            grouped[val] = []
        grouped[val].append(itunesTrackData)
    return grouped

def __aggregatePlayTimesForGroups__(grouped):
    for item in grouped.iteritems():
        counter = 0
        for track in item[1]:
            if itunes.KEY_PLAY_COUNT in track:
                counter += track[itunes.KEY_PLAY_COUNT] * track[itunes.KEY_TOTAL_TIME]
        yield item[0], counter

def totalPlayTime():
    totalPlayTime = 0
    for itunesTrackData in itunesCollection.find({itunes.KEY_PLAY_COUNT : {'$gt':0}}):
        trackPlayTime = itunesTrackData[itunes.KEY_TOTAL_TIME] * itunesTrackData[itunes.KEY_PLAY_COUNT]
        totalPlayTime += trackPlayTime
    totalHhmmss = timeutil.millisToHHMMSS(totalPlayTime)
    print LABEL_ROW_TEMPLATE.format('TOTAL', totalHhmmss[0], totalHhmmss[1], totalHhmmss[2])

def artistsMostPlayed():
    grouped = __groupItemsByKey__(itunesCollection, itunes.KEY_ARTIST)
    playTimes = __aggregatePlayTimesForGroups__(grouped)
    sortedByPlayTime = sorted(playTimes, key = operator.itemgetter(1))
    for item in sortedByPlayTime:
        hhmmss = timeutil.millisToHHMMSS(item[1])
        print LABEL_ROW_TEMPLATE.format(item[0], hhmmss[0], hhmmss[1], hhmmss[2])

def albumsMostPlayed():
    grouped = __groupItemsByKey__(itunesCollection, itunes.KEY_ALBUM)
    playTimes = __aggregatePlayTimesForGroups__(grouped)
    sortedByPlayTime = sorted(playTimes, key = operator.itemgetter(1))
    for item in sortedByPlayTime:
        hhmmss = timeutil.millisToHHMMSS(item[1])
        print LABEL_ROW_TEMPLATE.format(item[0], hhmmss[0], hhmmss[1], hhmmss[2])

#importItunes()
#printAllTracks()
#artistsMostPlayed()
albumsMostPlayed()
totalPlayTime()

