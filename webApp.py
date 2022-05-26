import io
from flask import Flask, render_template, request
from PIL import Image
import base64
from mongodatatest import *
import datetime as dt

app = Flask(__name__)

removed = []

def getpicture(item):
    tmode, tsize, tbytes = item["Thumb"]
    img = Image.frombytes(tmode, tsize, tbytes) 
    obj = io.BytesIO()
    try:
        img.save(obj, format='JPEG')
    except:
        rgb_img = img.convert("RGB")
        rgb_img.save(obj, format='JPEG')
    obj.seek(0)
    data = obj.read()
    data = base64.b64encode(data)
    data = data.decode()
    return data

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        removed.append(list(request.form.keys())[0])

    structure = get_similar_photos()

    for thesame in structure:
        for item in thesame:
            data = getpicture(item)
            item["data"] = data
            item['fCreate'] = dt.datetime.fromtimestamp(item['fCreate']).strftime('%A %-d %B %Y %-H:%M:%S')
            item['fModify'] = dt.datetime.fromtimestamp(item['fModify']).strftime('%A %-d %B %Y %-H:%M:%S')
            #, p11 = submitdisabled]}
    folderlist = get_pathes()
    toreturn = render_template('main.html', items = folderlist, listofphotos = structure)
    return toreturn

app.run(debug=True, port=8080)
