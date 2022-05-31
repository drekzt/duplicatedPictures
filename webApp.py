from flask import Flask, render_template, redirect
from PIL import Image
from mongodatatest import *
import datetime as dt

app = Flask(__name__)

removed = []

@app.route('/', methods=['POST', 'GET'])
def index():
    structure = get_similar_photos()
    for thesame in structure:
        for item in thesame:
            data = getpicture(item)
            item['data'] = data
            item['fCreate'] = dt.datetime.fromtimestamp(item['fCreate']).strftime('%A %-d %B %Y %-H:%M:%S')
            item['fModify'] = dt.datetime.fromtimestamp(item['fModify']).strftime('%A %-d %B %Y %-H:%M:%S')
            #, p11 = submitdisabled]}
    folderlist = get_pathes()
    toreturn = render_template('main.html', items = folderlist, listofphotos = structure)
    return toreturn

@app.route('/toggle/<id>')
def toggle_status(id):
    if id in removed:
        removed.remove(id)
    else:
        removed.append(id)
    return redirect('/')

app.run(debug=True, port=8080)
