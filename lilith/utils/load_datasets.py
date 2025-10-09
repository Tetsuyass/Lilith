import json
import re
import os
from datasets import Dataset
from routes import ROUTES

OUTPUT_PATHS = {
    "everyday": ROUTES["datasets"] + "/everyday",
    "comparia": ROUTES["datasets"] + "/comparia",
    "cfdd": ROUTES["datasets"] + "/cfdd",
}

DATASETS_PATHS = {
    "everyday": ROUTES["hd-datasets"] + "/EverydayConversations/train",
    "comparia": ROUTES["hd-datasets"] + "/Comparia/train",
    "cfdd": ROUTES["hd-datasets"] + "/CFDD/train",
}

def load_dataset(dataset_name):
    for file in os.listdir(DATASETS_PATHS[dataset_name]):
        if re.match(r"^data-\d+-of-\d+\.arrow$",file):
            dataset_ = Dataset.from_file(os.path.join(DATASETS_PATHS[dataset_name], file))
            dataset_.to_json(os.path.join(OUTPUT_PATHS[dataset_name], file.replace(".arrow", ".json")))


load_dataset("cfdd")
load_dataset("everyday")
load_dataset("comparia")
