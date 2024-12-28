
# Importamos las librerías que necesitamos

# Librerías de extracción de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime

# Importamos las librerías que necesitamos

# Librerías de extracción de datos
# -----------------------------------------------------------------------

# Importaciones:
# Beautifulsoup
from bs4 import BeautifulSoup

# Requests
import requests

import pandas as pd
import numpy as np

from time import sleep
import random
# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import os
import sys
from tqdm import tqdm 
sys.path.append("../")
from dotenv import load_dotenv
load_dotenv(dotenv_path="../")
#import streamlit as st
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth

def load_credentials():
    CLIENT_ID = os.getenv("client_ID")
    CLIENT_SECRET = os.getenv("client_Secret")
    REDIRECT_URI = "http://localhost:3000"
    SCOPES = (
        "user-read-private user-read-email user-library-read user-library-modify "
        "playlist-read-private playlist-read-collaborative playlist-modify-public "
        "playlist-modify-private user-top-read user-read-recently-played "
        "user-read-currently-playing user-read-playback-state user-modify-playback-state "
        "streaming user-follow-read user-follow-modify app-remote-control ugc-image-upload"
    )

    # Autenticación
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES
    ))

    return sp

def obtener_html_followers(user):
    # Iniciar el driver
    driver = webdriver.Chrome()
    url = f"https://open.spotify.com/user/{user}/followers"
    # Navegar a la página
    driver.get(url)
    sleep(2)
    #Maximizar ventana
    driver.maximize_window() 
    sleep(2)
    # Aceptar cookies	
    driver.find_element("css selector", "#onetrust-accept-btn-handler").click()
    # Esperar a que la página cargue
    sleep(2) 
    # Obtener el contenido completo después de cargar el JavaScript
    page_content = driver.page_source
            
    # Usar BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(page_content, "html.parser")
    driver.quit()
    return soup

def extraer_ids_usuario(sp,marca, html):
    print("Iniciando Extracción de Ids Usuario")
    followers = html.findAll("div",{"class":"Box__BoxComponent-sc-y4nds-0 kcRGDn Box-sc-1njtxi4-0 hscyXl aAYpzGljXQv1_zfopxaH Card"})
    id_followers = []
    for follower in followers:
        quitar_html = str(follower).split(" ")[1]
        quedarse_user = quitar_html.split("-")[-2]
        solo_id_user = quedarse_user.split(":")[-1]
        id_followers.append(solo_id_user)

    brand = []
    usernames = []
    users_id = []
    for user in tqdm(id_followers):
        try:
            usernames.append(sp.user(user)["display_name"])
            users_id.append(user)
            brand.append(marca)
        except:
            print(f"No se ha podido obtener el usuario {user}")

    df = pd.DataFrame({
        'brand': brand,
        'username': usernames,
        'user_id': users_id
    })
    return df

