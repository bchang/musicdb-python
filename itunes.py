'''
Created on Jan 10, 2013

@author: bchang
'''
from xmlutil import getChildrenByTagName, nextElement
from xml.dom import minidom
from dateutil.parser import parse

KEY_ARTIST = 'Artist'
KEY_ALBUM = 'Album'
KEY_NAME = 'Name'
KEY_PLAY_COUNT = 'Play Count'
KEY_TOTAL_TIME = 'Total Time'
KEY_TRACK_ID = 'Track ID'

def __findKeyWithKeyName__(parent, keyName):
    for key in getChildrenByTagName(parent, 'key'):
        if key.firstChild.data == keyName:
            return key
    return None

class ItunesTrack:
    def __init__(self, trackId, trackDict):
        self.trackId = trackId
        self.itunesData = dict()
        for key in getChildrenByTagName(trackDict, 'key'):
            keyName = key.firstChild.data
            valueType = nextElement(key).tagName
            if valueType == 'true' or valueType == 'false':
                value = bool(valueType)
            else:
                data = nextElement(key).firstChild.data
                if valueType == 'string':
                    value = data
                elif valueType == 'integer':
                    value = int(data)
                elif valueType == 'date':
                    value = parse(data)
                else:
                    raise Exception('unrecognized value type:', valueType)
            self.itunesData[keyName] = value

def parseItunesXml(xmlFile):
    xmldoc = minidom.parse(xmlFile)
    rootDict = getChildrenByTagName(xmldoc.documentElement, 'dict').next()
    
    tracksKey = __findKeyWithKeyName__(rootDict, 'Tracks')
    tracksDict = nextElement(tracksKey)

    tracks = []

    for trackKey in getChildrenByTagName(tracksDict, 'key'):
        trackId = trackKey.firstChild.data
        print trackId
        trackDict = nextElement(trackKey)
        track = ItunesTrack(trackId, trackDict)
        tracks.append(track)

    return tracks

def importItunesXml(xmlFile, itunesCollection):
    tracks = parseItunesXml(xmlFile)
    print 'done parsing ' + xmlFile + ' (' + str(len(tracks)) + ')'

    itunesCollection.remove()
    for track in tracks:
        itunesCollection.insert(track.itunesData)

    print 'done loading parsed tracks into db'
