import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
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

def load_qwen():
    print(f"{CLR_YELLOW}Loading Qwen2.5-0.5B (4-bit)...{CLR_RESET}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # Load Base Model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True
    )

    return model, tokenizer

def generate_answer(model_tokenizer_tuple, user_input, fact_context, score):
    model, tokenizer = model_tokenizer_tuple
    
    if score >= SIMILARITY_THRESHOLD:
        messages = [
            {
                "role": "system",
                "content": "You are the official KLE Tech University assistant. Answer ONLY using the facts provided below. If the facts do not contain the answer, say: I don't have that specific information right now. Keep your answer short and clear."
            },
            {
                "role": "user",
                "content": f"Facts:\n{fact_context}\n\nQuestion: {user_input}"
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": "You are the official KLE Tech University assistant. Politely say you don't have information on that topic and suggest the student visit the official website or contact the university office."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=200,
        do_sample=False
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def main():
    # 1. Load the Retrieval System (Sentence-BERT)
    kb, known_questions, embeddings, st_model = load_retrieval_system()
    
    # 2. Load the Generation System (Qwen LLM)
    qbox = load_qwen()
    
    # 3. Clean up VRAM for a fresh session
    torch.cuda.empty_cache()
    print(f"{CLR_GREEN}Semantic RAG Bot Ready!{CLR_RESET} Optimized for 4GB VRAM.")
    print(f"I now provide 100% accurate answers based on the latest university data.\n")
    
    while True:
        try:
            print(f"{CLR_CYAN}You:{CLR_RESET} ", end="")
            user_input = input()
            
            if user_input.lower().strip() in ["quit", "exit", "q"]:
                print(f"{CLR_BLUE}Bot:{CLR_RESET} Goodbye! 👋\n")
                break
                
            if not user_input.strip():
                continue
            
            # Step 1: Retrieval (Sentence-BERT RAG)
            score, fact_context = find_best_answer(user_input, kb, known_questions, embeddings, st_model)
            
            # Show thinking animation
            sys.stdout.write(f"{CLR_BLUE}Bot is thinking")
            for _ in range(3):
                time.sleep(0.2)
                sys.stdout.write(".")
                sys.stdout.flush()
            sys.stdout.write("\r" + " " * 20 + "\r")
            
            # Step 2: Generation
            response = generate_answer(qbox, user_input, fact_context, score)
            
            # Step 3: Output with typing effect
            typing_print(f"{CLR_BLUE}Bot:{CLR_RESET} ", response)
            
        except KeyboardInterrupt:
            print(f"\n{CLR_BLUE}Bot:{CLR_RESET} Session terminated. Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
