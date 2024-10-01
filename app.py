from flask import Flask, render_template
import os, re
from cover_dl import download_manga_cover  # Importez la fonction

app = Flask(__name__)

DATA_PATH = "static/content"

def scanFolder(url: str):
    print("Scanning folder...\n")
    file_list = []

    # Vérifie si le dossier existe
    if os.path.exists(url):
        # Liste les fichiers et dossiers dans le dossier spécifié
        for item in os.listdir(url):
            # Crée le chemin complet pour chaque élément
            item_path = os.path.join(url, item)
            # Ajoute l'élément à la liste
            file_list.append(item)
            print("found : " + item + "\n")  # Imprime chaque élément trouvé
        
        # Tri des chapitres par leur numéro
        file_list.sort(key=lambda x: list(map(int, re.findall(r'\d+', x))) if re.findall(r'\d+', x) else [0])
        
    else:
        print(f"err -> {url} doesn't exist")

    return file_list
    


@app.route("/")
def welcome():
    folders = scanFolder(DATA_PATH)
    return render_template("index.html", folders=folders)

@app.route("/r/<string:name>")
def view(name: str):
    chap = scanFolder(DATA_PATH+"/"+name)
    return render_template("view.html", name=name, chap=chap)

@app.route("/r/<string:name>/<string:chapter>")
def read(name: str, chapter: str):
    imgs = scanFolder(DATA_PATH+"/"+name+"/"+chapter)
    chap = scanFolder(DATA_PATH+"/"+name)
    return render_template("read.html", name=name, chapter=chapter, imgs=imgs, chap=chap)

if __name__ == "__main__":
    all_meta = scanFolder(DATA_PATH)
    for folder in all_meta:
        print("Get META for : " + folder)
        download_manga_cover(folder)
        
    
    app.run(debug=True, port=5000, host="0.0.0.0")
