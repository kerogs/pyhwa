from flask import Flask, render_template, redirect, url_for
import os, re, json
from cover_dl import download_manga_cover 

import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from app import *

DATA_PATH = "static/content"
DATA_PATH_META = "static/meta"
PyHwa_VERSION = "1.2-beta"

def start_flask():
    app.run(debug=False, port=5000, host="0.0.0.0", use_reloader=False)

# Classe de la fenêtre principale de l'application PyQt5
class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyHwa - v" + PyHwa_VERSION )  # Nom de la fenêtre PyQt5
        self.setGeometry(100, 100, 1200, 800)  # Taille et position de la fenêtre

        # Création de la vue du navigateur intégré
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))  # L'URL locale du serveur Flask

        # Disposition de l'interface
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # Configuration du widget principal
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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
    return render_template("index.html", folders=folders)


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
    # Lancer Flask dans un thread séparé
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Pause pour laisser Flask démarrer correctement
    time.sleep(1)

    # Lancer l'application PyQt5
    app = QApplication(sys.argv)
    web_app = WebApp()
    web_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
