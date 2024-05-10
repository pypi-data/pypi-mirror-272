import os

from dotenv import load_dotenv

from parea import Parea

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"))

dataset = p.get_collection(626)  # Replace DATASET_ID with the actual dataset ID

dataset.write_to_finetune_jsonl("finetune1.jsonl")
