import numpy as np
import json
import re
import random
import os
from routes import ROUTES

"""Normalisation et Fusion"""

#======= Config ========#

DATASETS_PATH = {
    "everyday": ROUTES["datasets"] + "/everyday",
    "comparia": ROUTES["datasets"] + "/comparia",
    "cfdd": ROUTES["datasets"] + "/cfdd"
}

RATIOS = {
    "everyday": 0.7,
    "comparia": 0.2,
    "cfdd": 0.1
}

OUTPUT_PATH = ROUTES["datasets"] + "/dataset.json"
SEED = 42
np.random.seed(SEED)

#======= Fonctions utils ========#


def load_json(path):
    """Charge un fichier .json sous forme de liste de dicts."""
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def normalize_cfdd(entry):
    """Normalise un texte CFDD en remplaçant les balises de locuteurs par [speakerNNN:]."""
    text = entry.get("text", "").strip()
    pattern = r"\[[A-Za-zÀ-ÖØ-öø-ÿ0-9_\-\.\s]+:\]"

    seen = {}
    counter = 0

    def replace_speaker(match):
        nonlocal counter
        tag = match.group(0)
        if tag not in seen:
            counter += 1
            seen[tag] = counter
        return f"[speaker{seen[tag]:03d}]:"

    text = re.sub(pattern, replace_speaker, text)
    return {"text": text, "source": "cfdd"}


def normalize_everyday(entry):
    """Convertit un prompt/completion en format [speaker001]/[speaker002]."""
    user = entry.get("prompt", "").strip()
    assistant = entry.get("completion", "").strip()

    text_parts = []
    if user:
        text_parts.append(f"[speaker001]: {user}")
    if assistant:
        text_parts.append(f"[speaker002]: {assistant}")

    text = "\n".join(text_parts)
    return {"text": text, "source": "everyday"}


def normalize_comparia(entry):
    """Convertit les conversations Comparia au format [speakerNNN]: ..."""
    pattern = r"^conversation_[a-zA-Z]+$"
    dialogues = []
    speakers = {}  # map role -> index
    counter = 0

    for key, messages in entry.items():
        if re.match(pattern, key):
            for msg in messages:
                role = msg.get("role", "").lower()
                content = msg.get("content", "").strip()
                if not content:
                    continue
                if role not in speakers:
                    counter += 1
                    speakers[role] = counter
                dialogues.append(f"[speaker{speakers[role]:03d}]: {content}")

    text = "\n".join(dialogues)
    return {"text": text, "source": "comparia"}



# =============== Chargement des données =============== #

datasets_ = {
    "everyday": {},
    "comparia": {},
    "cfdd": {},
}

for filename in os.listdir(DATASETS_PATH["everyday"]):
    if filename.endswith(".json"):
        datasets_["everyday"][filename] = load_json(DATASETS_PATH["everyday"] + "/" + filename)

for filename in os.listdir(DATASETS_PATH["comparia"]):
    if filename.endswith(".json"):
        datasets_["comparia"][filename] = load_json(DATASETS_PATH["comparia"] + "/" + filename)

for filename in os.listdir(DATASETS_PATH["cfdd"]):
    if filename.endswith(".json"):
        datasets_["cfdd"][filename] = load_json(DATASETS_PATH["cfdd"] + "/" + filename)

# =============== Echantillonage =============== #

# Combiner tous les shards en une seule liste par dataset
combined_datasets = {
    name: [entry for shard in shards.values() for entry in shard]
    for name, shards in datasets_.items()
}

# Normalisation et fusion pour tous les datasets
final = []

for name, data in combined_datasets.items():
    for entry in data:
        if name == "everyday":
            final.append(normalize_everyday(entry))
        elif name == "comparia":
            final.append(normalize_comparia(entry))
        elif name == "cfdd":
            final.append(normalize_cfdd(entry))

# Mélange final
random.shuffle(final)

# Nettoyage des retours à la ligne
final = [ {"text": re.sub(r"[\r\n]+", " ", f["text"]).strip(), "source": f["source"]} for f in final ]


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for row in final:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(f"✅ Dataset combiné sauvegardé dans {OUTPUT_PATH}")
print(f"Total d'entrées : {len(final)}")






