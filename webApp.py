import io
from flask import Flask, render_template, request
from PIL import Image
import base64
from mongodatatest import *
import datetime as dt

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        print(request.form)
    items = get_similar_photos()
    tdtemplate = render_template('tdtemplate.html')
    trstarttemplate = render_template('trstarttemplate.html')
    toreturn = ""
    for path in get_pathes():
        toreturn = toreturn + path + "<br>"
    toreturn = toreturn + '<table>'
    for thesame in items:
        toreturn = toreturn  + trstarttemplate.format(len(thesame))
        for item in thesame:
            tmode, tsize, tbytes = item["Thumb"]
            img = Image.frombytes(tmode, tsize, tbytes) 
            obj = io.BytesIO()             # file in memory to save image without using disk  #
            try:
                img.save(obj, format='JPEG')    # save in file (BytesIO)                           # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save
            except:
                rgb_img = img.convert("RGB")
                rgb_img.save(obj, format='JPEG')
            obj.seek(0)
            data = obj.read()              # get data from file (BytesIO)
            data = base64.b64encode(data)  # convert to base64 as bytes
            data = data.decode()           # convert bytes to string
            toinsert = tdtemplate.format(p1 = data, p2 = item["_id"], p3 = item['Path'], p4 = item['Name'], p5 = item['Size'], p6 = item['fSize'], p7 = item['Format'], p8 = item['Description'], p9 = dt.datetime.fromtimestamp(item['fCreate']).strftime('%A %-d %B %Y %-H:%M:%S'), p10 = dt.datetime.fromtimestamp(item['fModify']).strftime('%A %-d %B %Y %-H:%M:%S'))
            toreturn = toreturn + toinsert
        toreturn = toreturn  + "</tr>"
    toreturn = toreturn + '</table>'
    template = render_template('main.html').replace("</table>",toreturn)
    return template

app.run(debug=True, port=8080)
