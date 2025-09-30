from datasets import load_dataset
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Début du téléchargement des datasets...')
logging.info('Loading du dataset : CFDD...')
claire_french_dialogue = load_dataset("OpenLLM-France/Claire-Dialogue-French-0.1", sample_by="paragraph", streaming=False)
logging.info('Loading du dataset : Everyday Conversations...')
everyday_conversation = load_dataset("wraps/everyday-conversations-llama3.1-2k-french", sample_by="paragraph", streaming=False)
logging.info('Loading du dataset : Comparia Conversations...')
comparia_conversations = load_dataset("ministere-culture/comparia-conversations")

logging.info('Ecriture sur disque...')
logging.info('CFDD...')
claire_french_dialogue.save_to_disk("D:/1TRAVAIL/IA/datasets/CFDD")
logging.info('Everyday Conversations...')
everyday_conversation.save_to_disk("D:/1TRAVAIL/IA/datasets/EverydayConversations")
logging.info('Comparia Conversations...')
comparia_conversations.save_to_disk("D:/1TRAVAIL/IA/datasets/Comparia")

logging.info('Début du téléchargement des modèles...')
logging.info('Mistral-7B...')
model_name = 'mistral-7B'
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_directory = "D:/1TRAVAIL/IA/models/mistral7b_finetuned"

logging.info('Ecriture sur disque...')
logging.info('Traitement du modèle : Mistral-7B...')
# Sauvegarde du modèle
model.save_pretrained(save_directory)
logging.info('Traitement du tokenizer...')
# Sauvegarde du tokenizer
tokenizer.save_pretrained(save_directory)
