from flask import Flask, render_template, redirect, url_for
import os
import re
import json
import random
import webbrowser
import threading
import time
from cover_dl import download_manga_cover


DATA_PATH = "static/content"
DATA_PATH_META = "static/meta"
PYHWA_VERSION = "1.3-beta"


def start_flask():
    print("Démarrage du serveur Flask...")
    app.run(debug=False, port=5000, host="0.0.0.0", use_reloader=False)


def scanFolder(url: str):
    print("Scanning folder...\n")
    file_list = []

    if os.path.exists(url):
        for item in os.listdir(url):
            item_path = os.path.join(url, item)
            if item != ".gitkeep":
                file_list.append(item)
                print("found : " + item_path)
            else:
                print("ignored : " + item_path)

        file_list.sort(
            key=lambda x: (
                list(map(int, re.findall(r"\d+", x))) if re.findall(r"\d+", x) else [0]
            )
        )
    else:
        print(f"err -> {url} doesn't exist")

    return file_list


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
    genres = dataJSONauto.get("genres")
    description = dataJSONauto.get("description")

    return render_template(
        "view.html",
        name=name,
        chap=chap,
        lastChapter=lastChapter,
        chapterAlreadyRead=chapterAlreadyRead,
        coverURL=coverURL,
        genres=genres,
        description=description,
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


@app.route("/act/meta/")
def act_meta():
    print("act meta -> Going to auto update metadata")
    folders = scanFolder(DATA_PATH)
    for folder in folders:
        print("Get META for : " + folder)
        download_manga_cover(folder)

    return redirect(url_for("welcome"))


def main():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    time.sleep(1)
    
    webbrowser.open("http://127.0.0.1:5000")

    flask_thread.join()


if __name__ == "__main__":
    main()
