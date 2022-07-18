from cmath import sqrt
import os
from statistics import mean, stdev
import sys
from library import *
from PIL import Image, ImageStat
from pymongo import DESCENDING, ASCENDING
import re 

def get_data(pathtocheck,collection):
    for root, _, files in os.walk(pathtocheck):
        if not re.match('.*/\..*|^/dev.*|^/boot.*|^/opt.*|^/proc.*|^/run.*|^/tmp.*|^/usr.*|^/var.*|.*videothumbs|.*audiothumbs|.*Adobe Photoshop.*',root):
            for file in files:
                fullpath=os.path.join(root,file)
                try: 
                    img = Image.open(fullpath)
                    # stat = ImageStat.Stat(img)
                    thumb =  img.copy()
                    thumb.thumbnail((300, 300,), Image.LANCZOS)
                    thumbmongo = thumb.copy()
                    stat = ImageStat.Stat(thumbmongo)
                    boun = [img.width, img.height]
                    mean = stat.mean
                    mvctr = vector(stat.mean)
                    sdev = stat.stddev
                    svctr = vector(stat.stddev)
                    size = os.path.getsize(fullpath)
                    lastmod = os.path.getmtime(fullpath)
                    created = os.path.getctime(fullpath)
                    if (svctr > 0):
                        item = {
                        'Name' : file,
                        'Path' : root,
                        'Size' : boun,
                        'Mean' : mean,
                        'mVCTR' : mvctr,
                        'Stddev' : sdev,
                        'sVCTR' : svctr,
                        'Format' : img.format,
                        'Description' : img.format_description,
                        'fSize' : size,
                        'fCreate' : created,
                        'fModify' : lastmod,
                        'Thumb' : ( thumbmongo.mode, thumbmongo.size, thumbmongo.tobytes() ) }
                        collection.insert_one(item)
                        print (' Mean {}-{}. Dev {}-{}. {}'.format(mean,mvctr,sdev,svctr,file))
                        # print (' Size {}. Mean {}. Deviation {}. File {}. Path {} ({}/{}).'.format(boun,mean,sdev,file,root,created,lastmod))
                    else:
                        print ('\33[33m Not important {} \033[0m'.format(fullpath))
                except:
                    try:
                        print ('\33[31m Error {} on {}\033[0m'.format(sys.exc_info()[0],fullpath))
                    except:
                        print ('\33[31m Error {} on {}\033[0m'.format(sys.exc_info()[0],'File path too strange to write ;)'))
    return

def vector(triplet):
    toreturn = 0
    try:
        field0 = pow(triplet[0],2)
        field1 = pow(triplet[1],2)
        field2 = pow(triplet[2],2)
        toreturn = sqrt(field0+field1+field2).real
    except:
        pass
    return toreturn

def comparetriple(prev, current, which, acceptdiff):
    try:
        result = ((abs(current[which][0]-prev[which][0]) <= acceptdiff) and (abs(current[which][1]-prev[which][1]) <= acceptdiff) and (abs(current[which][2]-prev[which][2]) <= acceptdiff))
    except:
        result = False
    return result

def similarity(collection_name,factor):
    simmresult=[]
    previtem=[]
    # simornot = collection_name.find().sort(SIMILARITYFACTOR,DESCENDING)
    simornot = collection_name.find().sort(SIMILARITYFIELD,DESCENDING)
    for nextitem in simornot:
        if comparetriple(previtem,nextitem,SIMILARITYFIELD,factor):
            simmroot['similar'].append(nextitem['_id'])
        else:
            try:
                test = simmroot['similar'][0]
                simmresult.append(simmroot)
            except:
                pass
            finally:
                simmroot = { 'Item': nextitem['_id'], 'Path': nextitem['Path'], 'similar' : [] }
                previtem = nextitem
    try:
        test = simmroot['similar'][0]
        simmresult.append(simmroot)
    except:
        pass
    return simmresult

def simCollRecreate(factor):
    dbname = get_database()
    collection_name = dbname[PHOTOSCOLL]
    items2 = similarity(collection_name,factor)
    dbname.drop_collection(SIMILARCOLL)
    collection_name2 = dbname[SIMILARCOLL]
    collection_name2.insert_many(items2)

def photosCollRecreate():
    dbname = get_database()
    dbname.drop_collection(PHOTOSCOLL)
    collection_name = dbname[PHOTOSCOLL]
    get_data(ROOTDIR,collection_name)
    collection_name.create_index([(SIMILARITYFIELD, 1)])
    collection_name.create_index([(SIMILARITYFACTOR, 1)])

if __name__ == '__main__':
    photosCollRecreate()
    simCollRecreate(SIMILARITYSCALE)
