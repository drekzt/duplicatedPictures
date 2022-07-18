from asyncore import write
from click import open_file
from flask import Flask, render_template, redirect, request, url_for
from PIL import Image
from mongodatatest import *
import datetime as dt
import os
from pictures import simCollRecreate

app = Flask(__name__)
selectedRow = []

def createstructure():
    intstructure = get_similar_photos()
    for thesame in intstructure:
        for item in thesame:
            data = getpicture(item)
            item['data'] = data
            item['fCreate'] = dt.datetime.fromtimestamp(item['fCreate']).strftime('%A %-d %B %Y %-H:%M:%S')
            item['fModify'] = dt.datetime.fromtimestamp(item['fModify']).strftime('%A %-d %B %Y %-H:%M:%S')
        #, p11 = submitdisabled]}
    return intstructure

@app.route('/')
def index():
    toshow = structure[0:99]
    folderlist = get_pathes_from_structure(toshow, len(structure) )
    toreturn = render_template('main.html', items = folderlist, listofphotos = toshow)
    return toreturn

@app.route('/selected/<id>')
def select(id):
    intid = int(id)
    selectedRow = structure[intid]
    toreturn = render_template('selected.html', row = id, photocells = selectedRow)
    return toreturn

@app.route('/remove',methods = ['POST', 'GET'])
def delete():
    if request.method == 'POST':
        row = int(request.form["rowId"])
        for pict_no in request.form:
            try:
                col = int(pict_no)
                filetoremove = "{}/{}".format(structure[row][col]["Path"],structure[row][col]["Name"])
                print(filetoremove)
                try:
                    with open_file("./removed_pictures.log","a") as file_object:
                        file_object.write("{} - {}\n".format(dt.datetime.now(),filetoremove))
                    os.remove(filetoremove)
                except:
                    return redirect("/error")
            except:
                pass
        structure.pop(row)
        return redirect("/")
    else:
        return redirect("/")
    
@app.route('/recalculate',methods = ['POST', 'GET'])
def recalculate():
    if request.method == 'POST':
        try:
            factor = float(request.form['factor'])
        except:
            factor = SIMILARITYSCALE
        simCollRecreate(factor)
        global structure 
        structure = createstructure()
    return redirect("/")

@app.route("/error")
def doSomething():
    return render_template('error.html')

structure = createstructure()

app.run(debug=True, port=8080)
