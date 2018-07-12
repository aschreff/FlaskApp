from flask import Flask, render_template, request, redirect, Response, make_response, url_for, send_from_directory
from werkzeug.utils import secure_filename
import data
import json
import csv
import os

app = Flask(__name__)

class Struct(object): pass
global_variables = Struct()


UPLOAD_FOLDER = "static/sheet.csv"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

try:
    global_variables.recipes = data.readRecipes()
    global_variables.recipeDict = data.readRecipeDict()
    global_variables.mat = data.readWashMatrix()
except:
    print("No file yet chosen")


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/upload", methods = ["GET", "POST"])
def upload():
    if(request.method == "POST"):
        if("file" not in request.files):
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if(file.filename == ""):
            flash("No selected file")
            return redirect(request.url)
        if(file):
            filename = secure_filename(file.filename)
            file.save(app.config["UPLOAD_FOLDER"])
            global_variables.recipes = data.readRecipes()
            global_variables.recipeDict = data.readRecipeDict()
            global_variables.mat = data.readWashMatrix()
            return redirect(request.url)
    return render_template("upload.html")

@app.route("/prevresin")
def prev():
    return render_template("prevresin.html", recipes=global_variables.recipes)

@app.route("/nextresin/<string:id>/")
def nextresin(id):
    return render_template("nextresin.html", id = id, recipes=global_variables.recipes)

@app.route("/nextresin/<string:id>/wash/<string:id1>/<string:id2>")
def wash(id, id1, id2):
    return render_template("wash.html", prev=id1, next=id2, mat = global_variables.mat, recipeDict=global_variables.recipeDict)

@app.route("/nextresin/<string:id>/wash/<string:id1>/downloadDirs/<string:id2>/<string:id3>/<string:id4>")
def downloadDirs(id, id1, id2, id3, id4):
    prevResin = id2
    nextResin = id3
    wash = id4
    dirs = data.createDirections(wash)
    path = os.path.expanduser("~")+"/Desktop/%sDIRECTIONS.csv"%wash
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Previous Resin: %s" % prevResin])
        writer.writerow(["Next Resin: %s" % nextResin])
        writer.writerow([""])
        for elem in dirs:
            writer.writerow([elem])
    return render_template("end.html")


if(__name__ == "__main__"):
    app.run(debug = True, port = 4000)
