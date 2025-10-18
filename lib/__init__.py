# -*- coding: utf-8 -*-
"""
lib package for script.flix.rajada
Contém as bibliotecas internas para o motor de provedores do Flix Rajada.
"""

import os
import sys
import logging

# --- Caminhos base ---
ADDON_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RESOURCES_PATH = os.path.join(ADDON_PATH, "resources")
PROVIDERS_PATH = os.path.join(RESOURCES_PATH, "providers.json")

# --- Logging configurado para o Kodi ---
def get_logger(name="flix.rajada"):
    """
    Cria e retorna um logger configurado com prefixo do addon.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(f"[{name}] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# --- Inicialização de ambiente ---
sys.path.insert(0, ADDON_PATH)

# --- Importação preguiçosa de módulos importantes ---
try:
    import requests
except ImportError:
    raise ImportError("Biblioteca 'requests' não encontrada — necessária para scraping.")

# --- Utilidades globais ---
def join_path(*args):
    """Atalho para os.path.join com segurança"""
    return os.path.join(*args).replace("\\", "/")

def file_exists(path):
    """Verifica se um arquivo existe"""
    return os.path.exists(path)

# --- Log inicial ---
logger = get_logger()
logger.info("Pacote lib do Flix Rajada inicializado com sucesso.")
