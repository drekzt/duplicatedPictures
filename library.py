# library
import pathlib
from pathlib import Path

ROOTDIR = '/'
# ROOTDIR = Path.home().joinpath('Downloads')
PHOTOSCOLL= 'photos'
SIMILARCOLL = 'similars'
SIMILARITYFIELD = 'Stddev'
SIMILARITYFACTOR = 'sVCTR'
SIMILARITYSCALE = 0.1

#STDDEVCONST = 'Stddev'
#MEANCONST = 'Mean'

def get_database():
    from pymongo import MongoClient
    import pymongo

    CONNECTION_STRING = 'mongodb://127.0.0.1:2717/?authSource=admin'
    client = MongoClient(CONNECTION_STRING, connect=False)
    return client['photos']
