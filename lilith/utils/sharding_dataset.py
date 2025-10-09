import os
import json
import gzip
import re
import random
import logging
import sys
from routes import ROUTES

# === Paramètres ===
INPUT_FILE = ROUTES["datasets"] + "/dataset.json"  # JSONL (1 objet JSON par ligne)
OUTPUT_DIR = ROUTES["datasets-final"]
LINES_PER_SHARD = 100_000
SEED = 42
random.seed(SEED)

# === Initialisation ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

# === Vérification du fichier d’entrée ===
if not os.path.isfile(INPUT_FILE):
    logging.error(f"❌ Fichier introuvable : {INPUT_FILE}")
    sys.exit(1)

size_gb = os.path.getsize(INPUT_FILE) / (1024 ** 3)
logging.info(f"📥 Lecture du fichier d’entrée : {INPUT_FILE} ({size_gb:.2f} Go)")

# === Lecture et écriture par lots ===
line_count = 0
shard_index = 0
current_lines = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            logging.warning(f"Ligne ignorée (JSON invalide) : {e}")
            continue

        if "text" in entry:
            entry["text"] = re.sub(r"[\r\n]+", " ", entry["text"]).strip()

        current_lines.append(json.dumps(entry, ensure_ascii=False) + "\n")
        line_count += 1

        # Log toutes les 100k lignes
        if line_count % 100_000 == 0:
            logging.info(f"{line_count:,} lignes traitées...")

        # Écrire un shard quand on atteint la limite
        if len(current_lines) >= LINES_PER_SHARD:
            shard_path = os.path.join(OUTPUT_DIR, f"shard_{shard_index:05d}.jsonl.gz")
            with gzip.open(shard_path, "wt", encoding="utf-8") as fout:
                fout.writelines(current_lines)
            logging.info(f"✅ Shard {shard_index:05d} écrit ({len(current_lines):,} lignes).")
            current_lines = []
            shard_index += 1

# === Écriture du shard final ===
if current_lines:
    shard_path = os.path.join(OUTPUT_DIR, f"shard_{shard_index:05d}.jsonl.gz")
    with gzip.open(shard_path, "wt", encoding="utf-8") as fout:
        fout.writelines(current_lines)
    logging.info(f"✅ Shard final {shard_index:05d} écrit ({len(current_lines):,} lignes).")

# === Résumé final ===
total_shards = shard_index + (1 if current_lines else 0)
logging.info("-------------------------------------------------")
logging.info(f"📊 Total d’entrées traitées : {line_count:,}")
logging.info(f"📦 Total de shards créés : {total_shards}")
logging.info(f"📁 Fichiers enregistrés dans : {OUTPUT_DIR}")
logging.info("-------------------------------------------------")

# Vérification des tailles de shards
for file in sorted(os.listdir(OUTPUT_DIR)):
    path = os.path.join(OUTPUT_DIR, file)
    if os.path.isfile(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        logging.info(f"   {file} — {size_mb:.1f} Mo")

