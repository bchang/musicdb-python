'''
Created on Jan 14, 2013

@author: bchang
'''

ITUNES_XML = '/Users/bchang/Music/iTunes/iTunes Music Library.xml'
GMUSIC_USER = '<your google id>'
GMUSIC_PASSWORD = '<your google password>' # can use an application-specific password if you have 2-step verification

# a tuple of MongoDb userid and password - using None will use default host/port of localhost,27017
mongoCred = None
# a tuple of db userid and password
musicDbCred = None

doImport = False
