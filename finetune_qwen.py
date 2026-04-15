import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import os

# --- Configuration ---
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
DATASET_PATH = "kle_tech_dataset.jsonl"
OUTPUT_DIR = "kle_tech_qwen_adapter"

def finetune():
    import torch
    torch.cuda.empty_cache() # Clear any leftovers
    # 1. Load Model in 4-bit
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load Base Model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map={"": 0}, # Force to GPU 0 for stability
        low_cpu_mem_usage=True
    )

    # 2. Prepare for k-bit training
    model = prepare_model_for_kbit_training(model)

    # 3. LoRA Configuration
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # 4. Load Dataset
    def formatting_prompts_func(examples):
        instructions = examples["system"]
        inputs = examples["user"]
        outputs = examples["assistant"]
        texts = []
        for system, user, assistant in zip(instructions, inputs, outputs):
            # Llama 3 Chat Template Format
            text = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|>"
                f"<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|>"
                f"<|start_header_id|>assistant<|end_header_id|>\n\n{assistant}<|eot_id|>"
            )
            texts.append(text)
        return {"text": texts}

    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
    dataset = dataset.map(formatting_prompts_func, batched=True)

    # 5. Training Arguments (High-Intensity 0.5B Tuning)
    training_args = SFTConfig(
        output_dir=OUTPUT_DIR,
        dataset_text_field="text",
        max_length=256,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=8e-5, # High precision for 0.5B
        num_train_epochs=10, # Brute Force Learning
        bf16=True, 
        logging_steps=5,
        optim="paged_adamw_32bit",
        save_strategy="no", 
        lr_scheduler_type="cosine",
        report_to="none",
    )

    # 6. Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )

    print("Starting fine-tuning (Deep Training - 3 Epochs)...")
    trainer.train()

    # 7. Save Adapter
    print(f"Saving fine-tuned adapter to {OUTPUT_DIR}...")
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Fine-tuning complete!")

if __name__ == "__main__":
    finetune()
