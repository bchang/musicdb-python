'''
Created on Jan 10, 2013

@author: bchang
'''
import xmlutil
from xml.dom import minidom
from dateutil.parser import parse

KEY_ARTIST = 'Artist'
KEY_ALBUM = 'Album'
KEY_NAME = 'Name'
KEY_PLAY_COUNT = 'Play Count'
KEY_TOTAL_TIME = 'Total Time'
KEY_TRACK_ID = 'Track ID'

def __handleDictElement__(dictElement):
    d = dict()
    for keyElement in xmlutil.getChildrenByTagName(dictElement, 'key'):
        key = keyElement.firstChild.data
        valueElement = xmlutil.nextSiblingElement(keyElement)
        d[key] = __handleValueElement__(valueElement)
    return d

def __handleArrayElement__(arrayElement):
    a = []
    child = xmlutil.firstChildElement(arrayElement)
    while child is not None:
        a.append(__handleValueElement__(child))
        child = xmlutil.nextSiblingElement(child)
    return a

def __handleValueElement__(valueElement):
    valueType = valueElement.tagName
    if valueType == 'true' or valueType == 'false':
        return bool(valueType)
    elif valueType == 'dict':
        return __handleDictElement__(valueElement)
    elif valueType == 'array':
        return __handleArrayElement__(valueElement)
    else:
        data = valueElement.firstChild.data
        if valueType == 'string':
            return data
        elif valueType == 'data':
            return data.strip()
        elif valueType == 'integer':
            return int(data)
        elif valueType == 'date':
            return parse(data)
        else:
            raise Exception('unrecognized value type:', valueType)


def __parseItunesXml__(xmlFile):
    xmldoc = minidom.parse(xmlFile)
    assert xmldoc.documentElement.tagName == 'plist'
    rootDictElement = xmlutil.getChildrenByTagName(xmldoc.documentElement, 'dict').next()
    assert xmlutil.nextSiblingElement(rootDictElement) == None

    rootDict = __handleDictElement__(rootDictElement)

    tracksDict = rootDict['Tracks']

    return tracksDict

def importItunesXml(xmlFile, itunesCollection, keysCollection):
    tracksDict = __parseItunesXml__(xmlFile)
    print 'done parsing ' + xmlFile + ' (' + str(len(tracksDict)) + ')'

    itunesCollection.remove()
    keys = set()
    for track in tracksDict.itervalues():
        itunesCollection.insert(track)
        for key in track.iterkeys():
            keys.add(key)

    keysCollection.save({'_id' : 'itunes', 'keys' : list(keys)})
    print 'done loading parsed tracks into db'
