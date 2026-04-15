import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from chat import load_retrieval_system, find_best_answer, print_logo, typing_print, CLR_BLUE, CLR_CYAN, CLR_GREEN, CLR_YELLOW, CLR_RESET, SIMILARITY_THRESHOLD, FALLBACK_RESPONSES
import random
import time
import sys
import os

# --- Configuration ---
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
# --- Quantization Config for 4GB VRAM ---
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

def load_qwen(adapter_path="kle_tech_qwen_adapter"):
    print(f"{CLR_YELLOW}Loading Qwen2.5-0.5B (4-bit)...{CLR_RESET}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # Load Base Model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True
    )

    # Load Fine-tuned Adapter if it exists
    if os.path.exists(adapter_path):
        print(f"{CLR_YELLOW}Applying fine-tuned 'KLE Tech' brain...{CLR_RESET}")
        model = PeftModel.from_pretrained(model, adapter_path)
    else:
        print(f"{CLR_BLUE}No adapter found. Using base model.{CLR_RESET}")
        
    return model, tokenizer

def main():
    # 1. Load the Retrieval System (University Data)
    kb, k_q, v, m = load_retrieval_system()
    
    # 2. Load the Generation System (Qwen LLM + Adapter)
    model, tokenizer = load_qwen()
    
    print_logo()
    print(f"{CLR_GREEN}Fine-Tuned Hybrid Bot Ready!{CLR_RESET} Optimized for 4GB VRAM.")
    print(f"I am now specifically trained on KLE Tech data for better accuracy.\n")
    
    while True:
        try:
            print(f"{CLR_CYAN}You:{CLR_RESET} ", end="")
            user_input = input()
            
            if user_input.lower().strip() in ["quit", "exit", "q"]:
                print(f"{CLR_BLUE}Bot:{CLR_RESET} Goodbye! 👋\n")
                break
                
            if not user_input.strip():
                continue
            
            # Step 1: Retrieval (RAG)
            score, fact_context = find_best_answer(user_input, kb, k_q, v, m)
            
            # Show thinking animation
            sys.stdout.write(f"{CLR_BLUE}Bot is thinking")
            for _ in range(3):
                time.sleep(0.2)
                sys.stdout.write(".")
                sys.stdout.flush()
            sys.stdout.write("\r" + " " * 20 + "\r")
            
            if score < SIMILARITY_THRESHOLD:
                # If no university data found, let Qwen answer generally
                prompt_messages = [
                    {"role": "system", "content": "You are a helpful assistant for KLE Technological University. If you don't know something for sure, just be polite."},
                    {"role": "user", "content": user_input}
                ]
                text = tokenizer.apply_chat_template(
                    prompt_messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
            else:
                # If we found university data, inject it as context
                # ChatML Format with Strict Instruction
                text = (
                    f"<|im_start|>system\nYou are the official KLE Tech Assistant. Use ONLY the following verified university data "
                    f"to answer. If the data does not contain a specific number requested, state it clearly. "
                    f"Do NOT guess.\n\nVERIFIED DATA:\n{fact_context}<|im_end|>\n"
                    f"<|im_start|>user\n{user_input}<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
            
            # Step 2: Generation (LLM)
            model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

            generated_ids = model.generate(
                **model_inputs,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Step 3: Output with typing effect
            typing_print(f"{CLR_BLUE}Bot:{CLR_RESET} ", response)
            
        except KeyboardInterrupt:
            print(f"\n{CLR_BLUE}Bot:{CLR_RESET} Session terminated. Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
