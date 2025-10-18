# -*- coding: utf-8 -*-
"""
Módulo principal do Flix Rajada — responsável por buscar torrents via provedores.
Compatível com o sistema do Flix (script.flix.*).
"""

import os
import logging
from concurrent.futures import ThreadPoolExecutor

from xbmcgui import DialogProgressBG

from lib import PROVIDERS_PATH, get_logger
from lib.scraper import Scraper, ScraperRunner, default_session
from lib.utils import Title, Magnet, InvalidMagnet
from flix.provider import Provider, ProviderResult

logger = get_logger("flix.rajada.core")


# ----------------------------- #
#   Estrutura principal de busca
# ----------------------------- #

class RajadaResult:
    """Objeto que representa um resultado unificado de um ou mais provedores."""

    def __init__(self, scraper, result):
        self.providers = {scraper.name}
        self.title = result.get("title", "Sem título")
        self.magnet = result.get("magnet")
        self.seeds = result.get("seeds")
        self.leeches = result.get("leeches")
        self.size = result.get("size")
        self.icon = scraper.get_attribute("icon", default=None)
        self.color = scraper.get_attribute("color", default=None)

    def to_provider_result(self):
        """Converte o resultado para o formato ProviderResult, aceito pelo Flix."""
        label_parts = []

        if self.seeds:
            label_parts.append(f"[S:{self.seeds}]")
        if self.size:
            label_parts.append(f"[{self.size}]")

        label = " ".join(label_parts) or "[Link]"
        return ProviderResult(
            label=label,
            label2=self.title,
            icon=self.icon,
            url=f"plugin://plugin.video.torrest/play_magnet?magnet={self.magnet}",
        )


# ----------------------------- #
#   Execução principal
# ----------------------------- #

def perform_search(search_type, data):
    """
    Executa a busca usando os provedores configurados.
    Retorna uma lista de ProviderResult.
    """
    results = []
    with default_session() as session:
        scrapers = Scraper.get_scrapers(PROVIDERS_PATH, session=session)

        if not scrapers:
            logger.warning("Nenhum provedor configurado/enabled no providers.json")
            return []

        logger.info(f"Provedores carregados: {len(scrapers)}")

        with ProgressScraperRunner(scrapers) as runner:
            parsed = runner.parse(search_type, data)
            for scraper, scraper_results in parsed:
                for r in scraper_results:
                    try:
                        Magnet.from_string(r["magnet"])  # valida magnet
                        results.append(RajadaResult(scraper, r).to_provider_result())
                    except InvalidMagnet:
                        continue

    return results


# ----------------------------- #
#   Runner com barra de progresso
# ----------------------------- #

class ProgressScraperRunner(ScraperRunner):
    """Runner que exibe progresso durante a execução."""

    def __init__(self, scrapers, num_threads=8):
        super().__init__(scrapers, num_threads=num_threads)
        self._progress = DialogProgressBG()
        self._index = 0
        self._total = len(scrapers)
        self._progress.create("Flix Rajada", "Buscando torrents...")

    def before_result(self, scraper):
        self._index += 1
        percent = int(self._index * 100 / self._total)
        self._progress.update(percent, message=f"Verificando: {scraper.name}")

    def close(self):
        super().close()
        if self._progress:
            self._progress.close()
            self._progress = None


# ----------------------------- #
#   Provider compatível com o Flix
# ----------------------------- #

class RajadaProvider(Provider):
    """Classe principal do addon — chamada diretamente pelo Flix."""

    def search(self, query):
        return perform_search("query", query)

    def search_movie(self, tmdb_id, title, titles, year=None):
        return perform_search("movie", dict(tmdb_id=tmdb_id, title=Title(title, titles), year=year or ""))

    def search_show(self, tmdb_id, title, titles, year=None):
        return perform_search("show", dict(tmdb_id=tmdb_id, title=Title(title, titles), year=year or ""))

    def search_season(self, tmdb_id, title, season, titles):
        return perform_search("season", dict(tmdb_id=tmdb_id, title=Title(title, titles), season=season))

    def search_episode(self, tmdb_id, title, season, episode, titles):
        return perform_search("episode", dict(
            tmdb_id=tmdb_id, title=Title(title, titles), season=season, episode=episode))

    def resolve(self, provider_data):
        raise NotImplementedError("Resolve não é utilizado em RajadaProvider")


# ----------------------------- #
#   Execução direta (debug)
# ----------------------------- #

if __name__ == "__main__":
    test_data = dict(tmdb_id="12345", title="Deadpool", titles={}, year="2024")
    results = perform_search("movie", test_data)
    for r in results:
        print(r.label, "=>", r.url)
