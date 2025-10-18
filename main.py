# -*- coding: utf-8 -*-
import os
import sys
import logging
from xbmcaddon import Addon

# --- Inicialização básica ---
addon = Addon()
ADDON_ID = addon.getAddonInfo("id")
ADDON_NAME = addon.getAddonInfo("name")
ADDON_PATH = addon.getAddonInfo("path")
RESOURCES_PATH = os.path.join(ADDON_PATH, "resources")

sys.path.insert(0, os.path.join(ADDON_PATH, "lib"))

# --- Importa o núcleo do Rajada ---
from rajada_core import RajadaProvider

# --- Configura logging ---
logging.basicConfig(level=logging.INFO, format=f"[{ADDON_NAME}] %(message)s")
logger = logging.getLogger(ADDON_NAME)


def log(msg):
    """Log seguro para Kodi"""
    try:
        logger.info(msg)
    except Exception:
        pass


def run_provider():
    """
    Função principal.
    Recebe os argumentos do Flix (tipo de busca) e executa o provider.
    """
    if len(sys.argv) < 2:
        log("Nenhum argumento recebido - modo direto")
        return

    try:
        action = sys.argv[1]

        # Instancia o provedor principal
        provider = RajadaProvider()

        if action == "search_movie":
            tmdb_id = sys.argv[2]
            title = sys.argv[3]
            year = sys.argv[4] if len(sys.argv) > 4 else ""
            results = provider.search_movie(tmdb_id, title, year)

        elif action == "search_show":
            tmdb_id = sys.argv[2]
            title = sys.argv[3]
            year = sys.argv[4] if len(sys.argv) > 4 else ""
            results = provider.search_show(tmdb_id, title, year)

        elif action == "search_season":
            tmdb_id = sys.argv[2]
            title = sys.argv[3]
            season = sys.argv[4]
            results = provider.search_season(tmdb_id, title, season)

        elif action == "search_episode":
            tmdb_id = sys.argv[2]
            title = sys.argv[3]
            season = sys.argv[4]
            episode = sys.argv[5]
            results = provider.search_episode(tmdb_id, title, season, episode)

        elif action == "query":
            query = sys.argv[2]
            results = provider.search_query(query)

        else:
            log(f"Ação desconhecida: {action}")
            return

        # Retorna os resultados para o Flix
        if results:
            import json
            print(json.dumps([r.to_dict() for r in results]))
            log(f"Enviados {len(results)} resultados para o Flix.")
        else:
            log("Nenhum resultado encontrado.")

    except Exception as e:
        import traceback
        log(f"Erro ao executar o provedor: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_provider()
