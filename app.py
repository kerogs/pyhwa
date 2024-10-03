from flask import Flask, render_template, redirect, url_for, request
import os
import re
import json
import random
import webbrowser
import threading
import time
from python.helpers import download_manga_cover, scanFolder
from routes import *
# from python.cover_dl import download_manga_cover
# from python.page_def import *



def main():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    time.sleep(1)
    
    # webbrowser.open("http://127.0.0.1:" + str(PYHWA_PORT))

    flask_thread.join()


if __name__ == "__main__":
    main()
