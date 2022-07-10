import io
import base64
from library import *
from pymongo import DESCENDING, ASCENDING
from PIL import Image

dbname = get_database()

def get_aggregated_photos():
    collection_name = dbname[PHOTOSCOLL]

    stage_group = { 
        '$group': { 
            '_id': '$' + SIMILARITYFIELD, 
            'Count': { 
                '$sum': 1 
            } 
        } 
    }

    stage_filter = {
        '$match': {
            'Count': {
                '$gt': 1 
            }
        }
    }

    stage_sort = {
        '$sort': {
            'Path': DESCENDING
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
    collection_photos = dbname[SIMILARCOLL]
    pathes = []
    for path in collection_photos.distinct( 'Path' ):
        pathes.append(path)
    return pathes

def get_pathes_from_structure(structure,fulllistcnt):
    pathes = ['25 items from {}'.format(fulllistcnt)]
    for item in structure:
        for subitem in item:
            if subitem['Path'] not in pathes:
                pathes.append(subitem['Path'])
    return sorted(pathes)

def getpicture(item):
    tmode, tsize, tbytes = item['Thumb']
    img = Image.frombytes(tmode, tsize, tbytes) 
    obj = io.BytesIO()
    try:
        img.save(obj, format='JPEG')
    except:
        rgb_img = img.convert('RGB')
        rgb_img.save(obj, format='JPEG')
    obj.seek(0)
    data = obj.read()
    data = base64.b64encode(data)
    data = data.decode()
    return data


#test = get_similar_photos()
