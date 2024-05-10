# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 15:22:35 2022

@author: Jean Manuel González Mejía
@version: 0.0.13
@Description: Librería para la simplificación del código en proyectos de Python
@last_update: 2023-06-22
"""

try:

    import logging  # Libreria para logs
    import os
    from pathlib import Path
    import time
    import requests
    from urllib.parse import urlparse

    # Selenium
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.select import Select

    from bs4 import BeautifulSoup

    # Teradata
    import teradatasql
    from libgal.modules.Teradata import teradata
    from teradatasql import OperationalError as TeradataError

    # Variables de entorno
    from dotenv import load_dotenv

    # SQLALchemy
    from sqlalchemy import create_engine, Column, Integer, String, text, and_
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.exc import OperationalError as SQLAlchemyError
    from libgal.modules.SQLAlchemy import SQLAlchemy as sqlalchemy

    # Machine Learning
    from sklearn.base import BaseEstimator, TransformerMixin
    import numpy as np
    import pandas
    from collections import defaultdict
    from scipy.stats import ks_2samp
    from sklearn.metrics import roc_curve, roc_auc_score
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from libgal.modules.MLS import *


except ImportError as imp_err:
    # Freno ejecucion y devuelvo codigo de error
    raise ImportError(f"Error al importar libreria: {imp_err}")


def variables_entorno(path_env_file=None):
    """
    Descripción: Toma las variables de entorno del archivo .env o del SO
    Parámetro:
    - path_env_file (String):
    """

    if path_env_file != None and Path(path_env_file).exists():
        load_dotenv(path_env_file)
    else:
        from libgal.modules.Logger import Logger
        logger = Logger().get_logger()
        logger.warning(
            f"No se encontró el archivo {path_env_file} indicado para funcion variables_entorno() de libgal por lo "
            f"que se toma las variables de entorno de sistema."
        )

    return dict(os.environ)


class LoggerFormatException(Exception):
    pass


def logger(format_output="JSON", app_name=__name__, dir_name=None):
    """
    Descripción: Crea un nuevo logger
    Parámetro:
    - format_output (String): Tipo de Salida del Log (JSON, CSV)
    - app_name (String): Nombre de la aplicación para el log
    """
    from libgal.modules.Logger import Logger

    if format_output not in ['CSV', 'JSON']:
        raise LoggerFormatException("Tipo de formato de Log inválido. Formatos soportados (JSON y CSV).")

    # Create a custom logger
    _logger = Logger(format_output=format_output, app_name=app_name, dirname=str(dir_name))
    #_logger.set_format(format_output)
    _logger.get_logger().setLevel(logging.INFO)

    return _logger.get_logger()


def shutdown_logger():
    """
    Descripción: Cierra el log

    """
    print("La función shutdown_logger() se encuentra deprecada ya que el shutdown del logging se hace automáticamente.")
    pass


def firefox(webdriver_path, browser_path, url, hidden=False, tipo_archivo=None, ruta_descarga=None):

    """
    Descripción: Crea un cliente web para pruebas, scrapings y automatizaciones
    Parámetro:
    - webdriver_path (String): Path completo de la ruta y el archivo ejecutable del driver para el cliente web
    - browser_path (String): Path completo de la ruta y el archivo ejecutable del browser web
    - url (String): URL del sitio web a explorar.
    - hidden (Boolean): Indica si se oculta o no el cliente web. False por defecto.
    """

    options = webdriver.FirefoxOptions()
    options.binary_location = browser_path

    if hidden:
        options.add_argument("--headless")

    #profile = webdriver.FirefoxProfile()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)

    if ruta_descarga:
        options.set_preference('browser.download.dir', str(ruta_descarga))
        #options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

    if tipo_archivo.lower()=='pdf':
        options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
        options.set_preference('pdfjs.disabled',True)
    elif tipo_archivo.lower()=='txt':
        options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
    elif tipo_archivo.lower()=='png':
        options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/png')
    elif tipo_archivo.lower()=='jpg':
        options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')


    driver_service=Service(webdriver_path)

    web_browser = webdriver.Firefox(service=driver_service, options=options)
    web_browser.get(url)

    return web_browser


def html_parser(html):
    """
    Descripción: Parsea el código HTML para encontrar etiquetas específicas
    Parámetro:
    - html (String): código html a parsear
    """

    #soup = BeautifulSoup(html, 'html.parser')
    #return soup

    raise Exception("La función html_parser() se encuentra deprecada. Utilice la función request() en su lugar.")

def request(url, intentos=1, scraping=False):

    from libgal.modules.Logger import Logger
    _logger = Logger(format_output="CSV")
    _logger.get_logger().setLevel(logging.INFO)
    _log=_logger.get_logger()
    
    sesion=requests.sessions.Session()

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate", 
    #"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    "Dnt": "1", 
    "Host": urlparse(url).netloc, 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36", 
  }
    
    web=None

    intento = 0

    while intento < intentos:
        try:

            web=sesion.get(url ,headers=headers)

            if web != None:

                if scraping:
                    return BeautifulSoup(web.content, 'html.parser')
                else:
                    return web

        except requests.RequestException as e:
            _log.error(f"No se puede conectar a la URL especificada: {e}")
            intento += 1
            time.sleep(20)
        except requests.ConnectionError as e:
            _log.error(f"No se puede conectar a la URL especificada: {e}")
            intento += 1
            time.sleep(20)

    return False

