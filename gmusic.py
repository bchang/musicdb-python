'''
Created on Jan 12, 2013

@author: bchang
'''
from gmusicapi.api import Api

def importGmusicApi(email, password, gmusicCollection, keysCollection):
    api = Api()
    api.login(email, password)
    allSongs = api.get_all_songs()
    api.logout()

    gmusicCollection.remove()
    keys = set()
    for song in allSongs:
        gmusicCollection.insert(song)
        for key in song.iterkeys():
            keys.add(key)

    doc = { '_id' : 'gmusic', 'keys' : list(keys) }
    keysCollection.save(doc)
    print 'done importing', len(allSongs), 'gmusic songs into db'

'''
{u'comment': u'', u'rating': 0, u'lastPlayed': 1357428895753173, u'disc': 1, u'matchedId': u'Tfhuvxl32ki7phgtqqlywjw37wu', u'composer': u'Green Day', u'year': 2012, u'id': u'1aa46ccd-99a3-3156-b507-6c4fe791efd7', u'subjectToCuration': False, u'album': u'\xa1DOS! [Explicit]', u'title': u'F*** Time [Explicit]', u'deleted': False, u'albumArtist': u'Green Day', u'albumArtUrl': u'//lh5.googleusercontent.com/ZO6O1j4xKAlEGtz3aqITWgtURBgvXknlVmuU0m12l_lpy9UoG4-unHhQyWho=s130-c-e100', u'type': 6, u'titleNorm': u'f*** time [explicit]', u'track': 2, u'albumArtistNorm': u'green day', u'totalTracks': 13, u'beatsPerMinute': 0, u'genre': u'Alternative Rock', u'playCount': 0, u'creationDate': 1357428895753173, u'bitrate': 320, u'name': u'F*** Time [Explicit]', u'albumNorm': u'\xa1dos! [explicit]', u'artist': u'Green Day', u'url': u'', u'totalDiscs': 1, u'durationMillis': 166000, u'artistNorm': u'green day'}
'''
