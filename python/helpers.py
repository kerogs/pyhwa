import requests
import os
import json
import re
from config import logWriter, AUTO_META_SOURCE, DATA_PATH_META
import uuid


def scanFolder(url: str):
    print("Scanning folder...")
    file_list = []

    if os.path.exists(url):
        for item in os.listdir(url):
            item_path = os.path.join(url, item)
            if item != ".gitkeep":
                file_list.append(item)
                print("found : " + item_path)
                logWriter("(def scanFolder) found : " + item_path, "debug")
            else:
                print("ignored : " + item_path)
                logWriter("(def scanFolder) ignored : " + item_path, "debug")

        file_list.sort(
            key=lambda x: (
                list(map(int, re.findall(r"\d+", x))) if re.findall(r"\d+", x) else [0]
            )
        )
        logWriter("(def scanFolder) Success -> file_list : " + str(file_list), "debug")
    else:
        print(f"err -> {url} doesn't exist")
        logWriter("(def scanFolder) Error -> {url} doesn't exist", "error")

    return file_list


def auto_update_metadata(manga_name):

    # ? check if manga not already in meta
    if manga_name in os.listdir(DATA_PATH_META):
        logWriter(
            "(def auto_update_metadata) : already in meta",
            "warning",
        )
        return False

    if AUTO_META_SOURCE == "mangadex":
        logWriter(
            "(def auto_update_metadata) : "
            + AUTO_META_SOURCE
            + " (NAME : "
            + manga_name
            + ")",
            "info",
        )
        auto_meta_mangadex(manga_name)
    if AUTO_META_SOURCE == "anilist":
        logWriter(
            "(def auto_update_metadata) : "
            + AUTO_META_SOURCE
            + " (NAME : "
            + manga_name
            + ")",
            "info",
        )
        # auto_meta_anilist()
    else:
        logWriter("Unknown auto meta source : " + AUTO_META_SOURCE, "critical")


def auto_meta_mangadex(manga_name):
    logWriter("(def auto_meta_mangadex) AUTO META STARTING : " + manga_name, "debug")
    manga_name_encoded = manga_name.replace(" ", "%20")
    searchURL = f"https://api.mangadex.org/manga?title={manga_name_encoded}"
    logWriter("(def auto_meta_mangadex) REQUEST URL : " + searchURL, "debug")

    try:
        response = requests.get(searchURL)
        response.raise_for_status()
        data = response.json()
        logWriter("(def auto_meta_mangadex) DATA : " + str(data), "debug")

        if not data["data"]:
            logWriter(
                "(def auto_meta_mangadex) NO DATA FOUND : " + manga_name, "warning"
            )
            return False
        elif data["result"] != "ok":
            logWriter("(def auto_meta_mangadex) REQUEST ERROR : " + manga_name, "error")
            return False
        else:
            # ? REQUEST SUCCESS
            logWriter(
                "(def auto_meta_mangadex) REQUEST SUCCESS : " + manga_name, "debug"
            )

            dataJSON = data["data"][0]
        
            
            tags = [
                tag["attributes"]["name"]["en"] 
                for tag in dataJSON.get("attributes", {}).get("tags", [])
                if "name" in tag["attributes"] and "en" in tag["attributes"]["name"]
            ]

            # Construction de dataJSON
            dataJSONSave = {
                    "type": dataJSON["type"],
                    "source": "AUTO_META_SOURCE",  # Remplacez par la valeur appropriée
                    "attributes": {
                        "title": dataJSON["attributes"]["title"]["en"],  # Assurez-vous de prendre la valeur 'en'
                        "description": dataJSON["attributes"]["description"]["en"],  # Idem
                        "tags": tags,
                    }
                }
            
            logWriter("(def auto_meta_mangadex) DATAJSON data[data][0] OK ", "debug")

            # ? save info
            uid = str(uuid.uuid4())

            # ? make directory
            write_dir = DATA_PATH_META + "/" + manga_name
            os.makedirs(write_dir, exist_ok=True)
            logWriter(
                "(def auto_meta_mangadex) DATA JSON DIRECTORY CREATED : " + write_dir,
                "debug",
            )

            # ? save json
            write_json = DATA_PATH_META + "/" + manga_name + "/" + manga_name + ".json"
            with open(write_json, "w", encoding="utf-8") as json_file:
                json.dump(dataJSONSave, json_file, indent=4)
            if os.path.exists(write_json):
                logWriter(
                    "(def auto_meta_mangadex) SUCCESS DATA JSON FILE CREATED : "
                    + write_json,
                    "debug",
                )
            else:
                logWriter(
                    "(def auto_meta_mangadex) ERROR DATA JSON FILE NOT CREATED : "
                    + write_json,
                    "warning",
                )

            # ? save cover
            cover_art_relationships = dataJSON["relationships"]
            cover_id = next(
                (
                    rel["id"]
                    for rel in cover_art_relationships
                    if rel["type"] == "cover_art"
                ),
                None,
            )

            if cover_id:
                # Récupération des détails de la couverture
                cover_url = f"https://api.mangadex.org/cover/{cover_id}"
                cover_response = requests.get(cover_url)
                cover_response.raise_for_status()
                cover_data = cover_response.json()
                cover_filename = cover_data["data"]["attributes"].get("fileName")

                if cover_filename:
                    # Construction de l'URL de l'image de couverture
                    cover_image_url = f"https://uploads.mangadex.org/covers/{dataJSON['id']}/{cover_filename}"

                    # Téléchargement de l'image
                    img_response = requests.get(cover_image_url)
                    img_response.raise_for_status()

                    # Enregistrement de l'image
                    write_cover = (
                        DATA_PATH_META + "/" + manga_name + "/" + manga_name + ".jpg"
                    )
                    with open(write_cover, "wb") as cover_file:
                        cover_file.write(img_response.content)

                    logWriter(
                        "(def auto_meta_mangadex) COVER IMAGE SAVED : " + write_cover,
                        "debug",
                    )
                else:
                    logWriter(
                        "(def auto_meta_mangadex) NO COVER FILENAME FOUND : "
                        + manga_name,
                        "warning",
                    )
            else:
                logWriter(
                    "(def auto_meta_mangadex) NO COVER ID FOUND : " + manga_name,
                    "warning",
                )

    # ? error
    except requests.exceptions.HTTPError as http_err:
        logWriter("(def auto_meta_mangadex) HTTP ERROR : " + str(http_err), "error")
    except Exception as e:
        logWriter("(def auto_meta_mangadex) ERROR : " + str(e), "error")



# ! DEPRECATED
def download_manga_cover(manga_name):
    logWriter("DEPRECATED METHOD FOR AUTO META", "warning")
    manga_name_encoded = manga_name.replace(" ", "%20")
    search_url = f"https://api.mangadex.org/manga?title={manga_name_encoded}"
    print(f"Recherche de '{manga_name}'...")
    print(f"URL : {search_url}")

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()

        if not data["data"]:
            print(f"Aucun résultat trouvé pour '{manga_name}'.")
            return

        manga_info = data["data"][0]
        manga_id = manga_info["id"]

        # ? save info
        manga_details = {
            "title": manga_info["attributes"].get("title", {}).get("en", "N/A"),
            "alternative_titles": [
                alt_title.get("en", "N/A")
                for alt_title in manga_info["attributes"].get("altTitles", [])
            ],
            "description": manga_info["attributes"]
            .get("description", {})
            .get("en", "N/A"),
            "genres": [],
            "themes": [],
            "publication_year": manga_info["attributes"].get("year", "N/A"),
            "status": manga_info["attributes"].get("status", "N/A"),
            "cover_image_url": None,
            "alternative_images": [],
        }

        for tag in manga_info["attributes"].get("tags", []):
            tag_name = tag["attributes"].get("name", {}).get("en", "N/A")
            if tag["type"] == "tag":
                manga_details["genres"].append(tag_name)
            elif tag["type"] == "theme":
                manga_details["themes"].append(tag_name)

        cover_art_relationships = manga_info["relationships"]
        cover_id = next(
            (
                rel["id"]
                for rel in cover_art_relationships
                if rel["type"] == "cover_art"
            ),
            None,
        )

        if cover_id:
            cover_url = f"https://api.mangadex.org/cover/{cover_id}"
            cover_response = requests.get(cover_url)
            cover_response.raise_for_status()
            cover_data = cover_response.json()
            cover_filename = cover_data["data"]["attributes"].get("fileName", None)

            if cover_filename:
                manga_details["cover_image_url"] = (
                    f"https://uploads.mangadex.org/covers/{manga_id}/{cover_filename}"
                )

                img_response = requests.get(manga_details["cover_image_url"])
                img_response.raise_for_status()

                os.makedirs(f"static/meta/{manga_name}", exist_ok=True)

                image_path = os.path.join(
                    f"static/meta/{manga_name}", f"{manga_name}.jpg"
                )
                with open(image_path, "wb") as f:
                    f.write(img_response.content)

                print(f"Couverture téléchargée : {image_path}")
            else:
                print(f"Aucune couverture disponible pour '{manga_name}'.")
                return
        else:
            print(f"Aucune couverture trouvée pour '{manga_name}'.")
            return

        for relationship in cover_art_relationships:
            if relationship["type"] != "cover_art":
                try:
                    alt_cover_url = (
                        f"https://api.mangadex.org/cover/{relationship['id']}"
                    )
                    alt_cover_response = requests.get(alt_cover_url)
                    alt_cover_response.raise_for_status()
                    alt_cover_data = alt_cover_response.json()
                    alt_cover_filename = alt_cover_data["data"]["attributes"].get(
                        "fileName", None
                    )

                    if alt_cover_filename:
                        alternative_image_url = f"https://uploads.mangadex.org/covers/{manga_id}/{alt_cover_filename}"
                        manga_details["alternative_images"].append(
                            alternative_image_url
                        )
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de l'obtention d'une image alternative : {e}")

        json_filename = os.path.join(f"static/meta/{manga_name}", f"{manga_name}.json")
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(manga_details, json_file, ensure_ascii=False, indent=4)

        print(f"Détails sauvegardés dans : {json_filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
