from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from routes import ROUTES
from pathlib import Path

# === Configuration du modèle et tokenizer ===
model_name = ROUTES["hd-models"] + "/mistral7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_path = str(Path(ROUTES["datasets-final"]) / "train" / "*.jsonl.gz")
test_path = str(Path(ROUTES["datasets-final"]) / "test" / "*.jsonl.gz")
output_path = str(Path(ROUTES["models-discussion"]) / "lora-mistral7b")
logs_path = str(Path(ROUTES["temp"]) / "logs-lora")

# === Configuration de la quantification 8-bit avec offload CPU si VRAM insuffisante ===
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Préparer le modèle pour le fine-tuning LoRA sur quantized weights
model = prepare_model_for_kbit_training(model)

# === Configuration LoRA ===
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# === Chargement des shards JSONL ===
data_files = {
    "train": train_path,
    "test": test_path
}
dataset = load_dataset("json", data_files=data_files)

# Tokenisation (batched pour plus de rapidité)
tokenized = dataset.map(
    lambda x: tokenizer(
        x["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    ),
    batched=True,
    num_proc=4
)

# =========================================== Boucle d'entraînement ================================================== #
def main():
    training_args = TrainingArguments(
        output_dir=output_path,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        evaluation_strategy="steps",  # évaluation périodique
        eval_steps=200,
        logging_dir=logs_path,
        report_to="tensorboard",
        save_strategy="steps",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
    )

    trainer.train()

    # === Sauvegarder les poids LoRA dans un dossier dédié ===
    model.save_pretrained(output_path)


if __name__ == "__main__":
    main()
