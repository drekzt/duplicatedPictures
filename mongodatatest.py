from library import *
from pymongo import DESCENDING, ASCENDING
from PIL import Image

dbname = get_database()

def get_aggregated_photos():
    collection_name = dbname[PHOTOSCOLL]

    stage_group = { 
        "$group": { 
            "_id": "$" + SIMILARITYFIELD, 
            "Count": { 
                "$sum": 1 
            } 
        } 
    }

    stage_filter = {
        "$match": {
            "Count": {
                    "$gt": 1 
            }
        }
    }

    stage_sort = {
        "$sort": {
            "Path": DESCENDING
        }
    }

    projection = { '_id' : 0, 'Path' : 1, 'Name': 1, 'Thumb': 1, SIMILARITYFIELD : 1}

    pipeline = [stage_group, stage_filter, stage_sort]
    item_grouped = collection_name.aggregate(pipeline)
    before=''
    images = []
    for item in item_grouped:
        id=item['_id']
        simple_find = { SIMILARITYFIELD: id } 
        item_details = collection_name.find(simple_find,projection) 
        for detail in item_details:
            if before != detail[SIMILARITYFIELD]:
                #print("-" * 20)
                #print("{} : {}".format(whichfield,detail[whichfield]))
                before = detail[SIMILARITYFIELD]
                try:
                    images.append(sameimages)
                except:
                    pass
                sameimages = []
            sameimages.append(detail)
            #print("File {} at {}".format(detail['Name'], detail['Path']))
    return images

def get_similar_photos():
    collection_similar = dbname[SIMILARCOLL]
    collection_photos = dbname[PHOTOSCOLL]
    images = []
    for item in collection_similar.find().sort('Path',ASCENDING):
        sameimages = [ collection_photos.find_one({ '_id' : item['Item']}) ]
        for next in item['similar']:
            sameimages.append( collection_photos.find_one({ '_id' : next}) )
        images.append(sameimages)
    return images

def get_pathes():
    collection_photos = dbname[PHOTOSCOLL]
    pathes = []
    for path in collection_photos.distinct( "Path" ):
        pathes.append(path)
    return pathes

#test = get_similar_photos()