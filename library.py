# library
import pathlib
from pathlib import Path

ROOTDIR = '/'
# ROOTDIR = Path.home().joinpath('Downloads','iCloud Photos','Test')
# ROOTDIR = Path.home().joinpath('Downloads')
# ROOTDIR = Path.home()
PHOTOSCOLL= 'photos'
SIMILARCOLL = 'similars'
# SIMILARITYFIELD = 'Stddev'
SIMILARITYFIELD = 'Mean'
SIMILARITYFACTOR = 'sVCTR'
SIMILARITYSCALE = 0.4

#STDDEVCONST = 'Stddev'
#MEANCONST = 'Mean'

def get_database():
    from pymongo import MongoClient
    import pymongo

    CONNECTION_STRING = 'mongodb://127.0.0.1:2717/?authSource=admin'
    client = MongoClient(CONNECTION_STRING, connect=False)
    return client['photos']
