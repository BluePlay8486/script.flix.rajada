# -*- coding: utf-8 -*-
"""
Flix Rajada - utils.py
Funções utilitárias usadas em todo o sistema de scraping.
"""

import re
import unicodedata
import hashlib
import logging
from urllib.parse import quote_plus, unquote_plus

logger = logging.getLogger("flix.rajada.utils")

# ---------------------------------------------------------
# Texto e Normalização
# ---------------------------------------------------------

def normalize_text(text):
    """Remove acentos, símbolos e espaços duplicados."""
    if not text:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-zA-Z0-9\s\.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def slugify(text):
    """Gera um slug seguro para URLs."""
    return quote_plus(normalize_text(text).lower().replace(" ", "-"))


def clean_html(text):
    """Remove tags HTML simples."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


# ---------------------------------------------------------
# Tamanhos e conversões
# ---------------------------------------------------------

def sizeof_fmt(num, suffix="B"):
    """Formata bytes em tamanho legível (ex: 1.4 GB)."""
    if num is None:
        return "?"
    try:
        num = float(num)
    except ValueError:
        return str(num)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} E{suffix}"


def parse_size(size_str):
    """Converte texto como '1.2 GB' → bytes (int)."""
    if not size_str:
        return 0
    try:
        size_str = size_str.strip().upper().replace(",", ".")
        num = float(re.findall(r"[\d\.]+", size_str)[0])
        if "K" in size_str:
            num *= 1024
        elif "M" in size_str:
            num *= 1024 ** 2
        elif "G" in size_str:
            num *= 1024 ** 3
        elif "T" in size_str:
            num *= 1024 ** 4
        return int(num)
    except Exception:
        return 0


# ---------------------------------------------------------
# Identificadores / Hashes
# ---------------------------------------------------------

def md5_hash(text):
    """Retorna hash MD5 de um texto."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def safe_filename(text):
    """Remove caracteres inválidos para nomes de arquivos."""
    text = normalize_text(text)
    return re.sub(r"[\\/:\*\?\"<>\|]", "", text)


# ---------------------------------------------------------
# URL helpers
# ---------------------------------------------------------

def safe_url(url):
    """Escapa URL sem quebrar o esquema base."""
    try:
        return quote_plus(url, safe=":/?&=%")
    except Exception:
        return url


def decode_url(url):
    """Decodifica URLs percent-encoded."""
    try:
        return unquote_plus(url)
    except Exception:
        return url


# ---------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------

def debug_log(name, value):
    """Log detalhado no modo de desenvolvimento."""
    logger.debug(f"[Rajada Debug] {name}: {value}")


# ---------------------------------------------------------
# Checagens simples
# ---------------------------------------------------------

def is_magnet(url):
    """Verifica se a URL é um magnet link."""
    return str(url).startswith("magnet:?xt=")


def is_torrent_file(url):
    """Verifica se a URL é de arquivo .torrent."""
    return str(url).lower().endswith(".torrent")


def guess_quality(title):
    """Tenta adivinhar a qualidade (ex: 1080p, 4K)."""
    title = title.lower()
    if "2160" in title or "4k" in title:
        return "4K"
    if "1080" in title:
        return "1080p"
    if "720" in title:
        return "720p"
    if "480" in title:
        return "480p"
    return "SD"


# ---------------------------------------------------------
# Exemplo de uso
# ---------------------------------------------------------

if __name__ == "__main__":
    print("🔧 Teste utils.py")
    sample = "Filme: O Poderoso Chefão (1972)"
    print("Normalizado:", normalize_text(sample))
    print("Slug:", slugify(sample))
    print("Size:", sizeof_fmt(1073741824))
    print("Quality:", guess_quality(sample))
