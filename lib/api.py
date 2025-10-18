# -*- coding: utf-8 -*-
"""
Flix Rajada - API de comunicação
Responsável por intermediar as chamadas entre o Flix e o sistema interno do Rajada.
"""

import json
import logging
from lib.rajada_core import RajadaProvider

logger = logging.getLogger("flix.rajada.api")
provider = RajadaProvider()


def _safe_json(data):
    """Garante que a resposta seja um JSON válido."""
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Erro ao converter resposta em JSON: {e}")
        return json.dumps({"error": str(e)})


# ------------------------------
# Rotas de busca principais
# ------------------------------

def search_movie(params):
    """
    Busca torrents de filmes.
    Espera parâmetros:
        {
            "tmdb_id": "12345",
            "title": "Matrix",
            "titles": {},
            "year": 1999
        }
    """
    try:
        results = provider.search_movie(
            tmdb_id=params.get("tmdb_id"),
            title=params.get("title"),
            titles=params.get("titles", {}),
            year=params.get("year"),
        )
        return _safe_json([r.__dict__ for r in results])
    except Exception as e:
        logger.exception("Erro ao buscar filme:")
        return _safe_json({"error": str(e)})


def search_show(params):
    """
    Busca torrents de séries completas.
    """
    try:
        results = provider.search_show(
            tmdb_id=params.get("tmdb_id"),
            title=params.get("title"),
            titles=params.get("titles", {}),
            year=params.get("year"),
        )
        return _safe_json([r.__dict__ for r in results])
    except Exception as e:
        logger.exception("Erro ao buscar série:")
        return _safe_json({"error": str(e)})


def search_season(params):
    """
    Busca torrents de temporadas completas.
    """
    try:
        results = provider.search_season(
            tmdb_id=params.get("tmdb_id"),
            title=params.get("title"),
            season=params.get("season"),
            titles=params.get("titles", {}),
        )
        return _safe_json([r.__dict__ for r in results])
    except Exception as e:
        logger.exception("Erro ao buscar temporada:")
        return _safe_json({"error": str(e)})


def search_episode(params):
    """
    Busca torrents de episódios.
    """
    try:
        results = provider.search_episode(
            tmdb_id=params.get("tmdb_id"),
            title=params.get("title"),
            season=params.get("season"),
            episode=params.get("episode"),
            titles=params.get("titles", {}),
        )
        return _safe_json([r.__dict__ for r in results])
    except Exception as e:
        logger.exception("Erro ao buscar episódio:")
        return _safe_json({"error": str(e)})


# ------------------------------
# Rota genérica de query
# ------------------------------

def search_query(params):
    """
    Busca livre por texto (título, termo, etc).
    """
    try:
        query = params.get("query") or params.get("title")
        if not query:
            return _safe_json({"error": "Faltando campo 'query'"})

        results = provider.search(query)
        return _safe_json([r.__dict__ for r in results])
    except Exception as e:
        logger.exception("Erro ao executar busca livre:")
        return _safe_json({"error": str(e)})


# ------------------------------
# Interface CLI (debug local)
# ------------------------------

if __name__ == "__main__":
    import sys
    import pprint

    print("🔍 Teste rápido - Rajada API")

    args = sys.argv[1:]
    if not args:
        print("Uso: python api.py 'Matrix 1999'")
        sys.exit(0)

    query = " ".join(args)
    response = search_query({"query": query})

    print("\nResultado:")
    pprint.pprint(json.loads(response))
