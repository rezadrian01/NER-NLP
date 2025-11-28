"""
Configuration file for Wayang NER and Knowledge Graph Builder
Author: Ahmad Reza Adrian
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Dataset configuration
DATASET_PATHS = [
    DATA_DIR / "wayang_stories_dataset.csv",
    DATA_DIR / "sitija_takon_bapa_dataset.csv"
]
DATASET_PATH = DATA_DIR / "wayang_stories_dataset.csv"  # Default/primary dataset
TEXT_COLUMN = "isi_teks"  # Default column for wayang_stories_dataset

# Column mapping for different datasets
DATASET_COLUMNS = {
    "wayang_stories_dataset.csv": {
        "text": "isi_teks",
        "title": "judul",
        "source": "wayang_stories"
    },
    "sitija_takon_bapa_dataset.csv": {
        "text": "Content",
        "title": "Title",
        "source": "sitija_takon_bapa"
    }
}

# NER configuration
NER_MODEL = "xx_ent_wiki_sm"  # Multilingual spaCy model
# Alternative: use IndoBERT from transformers
INDOBERT_MODEL = "indobenchmark/indobert-base-p1"

# Entity types
ENTITY_TYPES = ["PERSON", "LOC", "ORG", "EVENT", "OBJECT"]

# Relation patterns (Indonesian)
RELATION_PATTERNS = {
    "child_of": [
        r"putra\s+(?:dari\s+)?(\w+)",
        r"putri\s+(?:dari\s+)?(\w+)",
        r"anak\s+(?:dari\s+)?(\w+)",
        r"adalah\s+putra\s+(\w+)",
        r"adalah\s+putri\s+(\w+)"
    ],
    "married_to": [
        r"menikah\s+dengan\s+(\w+)",
        r"suami\s+dari\s+(\w+)",
        r"istri\s+dari\s+(\w+)",
        r"pasangan\s+(\w+)",
        r"rabi\s+(?:dengan\s+)?(\w+)"
    ],
    "fought_with": [
        r"bertempur\s+(?:dengan|melawan)\s+(\w+)",
        r"bertarung\s+(?:dengan|melawan)\s+(\w+)",
        r"melawan\s+(\w+)",
        r"perang\s+(?:dengan|melawan)\s+(\w+)"
    ],
    "killed_by": [
        r"tewas\s+(?:di tangan|oleh)\s+(\w+)",
        r"gugur\s+(?:di tangan|oleh)\s+(\w+)",
        r"dibunuh\s+(?:oleh\s+)?(\w+)",
        r"mati\s+(?:di tangan|oleh)\s+(\w+)"
    ],
    "sibling_of": [
        r"kakak\s+(?:dari\s+)?(\w+)",
        r"adik\s+(?:dari\s+)?(\w+)",
        r"saudara\s+(?:dari\s+)?(\w+)"
    ],
    "ruled_in": [
        r"raja\s+(?:di|dari)\s+(\w+)",
        r"prabu\s+(?:di|dari)\s+(\w+)",
        r"kerajaan\s+(\w+)",
        r"memerintah\s+(?:di\s+)?(\w+)"
    ],
    "died_in": [
        r"gugur\s+(?:dalam|di)\s+(\w+)",
        r"tewas\s+(?:dalam|di)\s+(\w+)",
        r"mati\s+(?:dalam|di)\s+(\w+)"
    ]
}

# Graph visualization settings
GRAPH_SETTINGS = {
    "height": "800px",
    "width": "100%",
    "bgcolor": "#222222",
    "font_color": "white",
    "node_color": "#4a90e2",
    "edge_color": "#cccccc"
}

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
