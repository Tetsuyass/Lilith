"""
Initialiser la logique (modèle, pipe, nlp etc...)
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch

# MISTRAL 7B -- LOADING

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

# FIN MISTRAL7B Loading --


def load_model_discussion(model_name, bonobo_config):

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bonobo_config,
        dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        dtype=torch.bfloat16,
        device_map="auto"
    )
    print("modèle chargé : " + model_name)
    return pipe
