from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

def load_model():
    model_name = "D:/1TRAVAIL/IA/models/mistral7b"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
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

    return pipe

def process_answer(prompt, pipe):
    sequences = pipe(
        prompt,
        do_sample=True,
        max_new_tokens=100,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
    )
    gen = sequences[0]['generated_text']
    return gen
