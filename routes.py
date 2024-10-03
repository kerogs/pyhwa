from flask import Flask, render_template, redirect, url_for, request
import os
import re
import json
import random
import webbrowser
from python.helpers import auto_update_metadata, scanFolder
from config import *

def start_flask():
    print("======================>")
    print("PyHwa " + PYHWA_VERSION)
    print("PyHwa Port : " + str(PYHWA_PORT))
    print("DATA_PATH : " + DATA_PATH)
    print("DATA_PATH_META : " + DATA_PATH_META)
    print("EN_LOGS : " + str(EN_LOGS))
    
    if(PYHWA_LOCAL_NETWORK):
        print("Pyhwa Local Network : ON")
        PHLNA = "0.0.0.0"
    else:
        print("Pyhwa Local Network : OFF")
        PHLNA = "127.0.0.1"
        
    webbrowser.open("http://127.0.0.1:" + str(PYHWA_PORT))
    print("======================>\n")
    logWriter("Starting PyHwa server...", "info")
    app.run(debug=True, port=PYHWA_PORT, host=PHLNA, use_reloader=False)
    

app = Flask(__name__)


@app.route("/")
def welcome():
    folders = scanFolder(DATA_PATH)
    results = []  # Liste qui contiendra les données de chaque dossier

    # Charger les données de chaque dossier
    for folder in folders:
        # Chemin du fichier JSON
        dataJSON_Path = os.path.join(DATA_PATH_META, folder, "localmeta.json")
        dataJSON = {}

        # Vérifier si le fichier JSON existe et le charger
        if os.path.exists(dataJSON_Path):
            with open(dataJSON_Path, "r", encoding="utf-8") as f:
                dataJSON = json.load(f)
        else:
            dataJSON = {"lastchapter": None, "chapterRead": {}}

        if os.path.exists(DATA_PATH_META + "/" + folder + "/" + folder + ".json"):
            with open(
                DATA_PATH_META + "/" + folder + "/" + folder + ".json",
                "r",
                encoding="utf-8",
            ) as f:
                dataJSONfolder = json.load(f)

        # Ajouter l'URL de l'image
        image_url = DATA_PATH_META + "/" + folder + "/" + folder + ".jpg"

        # Ajouter les informations dans un dictionnaire pour ce dossier
        folder_data = {
            "folder": folder,
            "metadata": dataJSON,
            "image_url": image_url,
            "dataJSONfolder": dataJSONfolder,
        }

        # Ajouter les données du dossier à la liste des résultats
        results.append(folder_data)

    # Créer une liste aléatoire de 5 dossiers maximum
    randfolders = random.sample(results, min(5, len(results)))

    # Retourner les résultats à la page HTML
    
    logWriter("index.html -> " + str(results))
    return render_template("index.html", folders=results, randfolders=randfolders)


@app.route("/r/<string:name>")
def view(name: str):
    # ? Prepare DATA
    chap = scanFolder(DATA_PATH + "/" + name)

    # ? Get data from JSON
    dataJSON_Path = os.path.join(DATA_PATH_META, name, "localmeta.json")
    dataJSON = {}
    if os.path.exists(dataJSON_Path):
        with open(dataJSON_Path, "r", encoding="utf-8") as f:
            dataJSON = json.load(f)
    else:
        dataJSON = {"lastchapter": None, "chapterRead": {}}

    lastChapter = dataJSON.get("lastChapter")
    chapterAlreadyRead = dataJSON.get("chapterRead", {}).keys()

    # ? get preview
    coverURL = DATA_PATH_META + "/" + name + "/" + name + ".jpg"

    # ? get other data
    dataJSONauto = DATA_PATH_META + "/" + name + "/" + name + ".json"
    if os.path.exists(dataJSONauto):
        with open(dataJSONauto, "r", encoding="utf-8") as f:
            dataJSONauto = json.load(f)
    else:
        dataJSONauto = {}

    return render_template(
        "view.html",
        name=name,
        chap=chap,
        lastChapter=lastChapter,
        chapterAlreadyRead=chapterAlreadyRead,
        coverURL=coverURL,
        dataJSONauto=dataJSONauto,
        dataJSON=dataJSON
    )


@app.route("/r/<string:name>/<string:chapter>")
def read(name: str, chapter: str):
    # ? Prepare DATA
    imgs = scanFolder(DATA_PATH + "/" + name + "/" + chapter)
    chap = scanFolder(DATA_PATH + "/" + name)
    chapterNumber = re.findall(r"\d+", chapter)
    if chapterNumber:
        chapterNbr = chapterNumber[0]

    # ? JSON
    dataJSON_Path = os.path.join(DATA_PATH_META, name, "localmeta.json")

    dataJSON = {}
    if os.path.exists(dataJSON_Path):
        with open(dataJSON_Path, "r", encoding="utf-8") as f:
            dataJSON = json.load(f)
    dataJSON["lastChapter"] = chapter
    if "chapterRead" not in dataJSON:
        dataJSON["chapterRead"] = {}
    dataJSON["chapterRead"][chapter] = chapter
    with open(dataJSON_Path, "w", encoding="utf-8") as f:
        json.dump(dataJSON, f, indent=4, ensure_ascii=False)

    # ? load page
    return render_template(
        "read.html",
        name=name,
        chapter=chapter,
        imgs=imgs,
        chap=chap,
        chapterNumber=chapterNbr,
    )


@app.route("/act/meta")
def act_meta():
    print("act meta -> Going to auto update metadata")
    folders = scanFolder(DATA_PATH)
    for folder in folders:
        print("Get META for : " + folder)
        auto_update_metadata(folder)
        # download_manga_cover(folder)
        
        
    logWriter("Prepare auto update metadata (from URL)", "info")
    return redirect(url_for("welcome"))

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/unread")
def unread():
    return render_template("unread.html")

@app.route("/continue")
def continueread():
    return render_template("continue.html")