import torch
import os
import json
import random
import sys
import time

from sentence_transformers import SentenceTransformer, util

# --- ANSI Color Codes ---
CLR_BLUE = "\033[1;34m"
CLR_CYAN = "\033[1;36m"
CLR_GREEN = "\033[0;32m"
CLR_YELLOW = "\033[1;33m"
CLR_RED = "\033[1;31m"
CLR_RESET = "\033[0m"

def typing_print(prefix, text):
    """Prints text with a typing effect."""
    sys.stdout.write(prefix)
    sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01) # Speed of typing
    sys.stdout.write("\n\n")
    sys.stdout.flush()

def print_logo():
    logo = f"""
{CLR_RED}  _  ___      ______   _______ ______ _____ _    _ 
 | |/ / |    |  ____| |__   __|  ____/ ____| |  | |
 | ' /| |    | |__       | |  | |__ | |    | |__| |
 |  < | |    |  __|      | |  |  __|| |    |  __  |
 | . \\| |____| |____     | |  | |___| |____| |  | |
 |_|\\_\\______|______|    |_|  |______\\_____|_|  |_| {CLR_RESET}
    
 {CLR_YELLOW}>>> KLE Tech Hybrid RAG Chatbot{CLR_RESET}
    """
    print(logo)

# Similarity threshold
SIMILARITY_THRESHOLD = 0.35

FALLBACK_RESPONSES = [
    "I'm sorry, I don't have specific information about that topic yet. I can help you with questions about KLE Tech's courses, placements, fees, and campus details.",
    "That's a great question, but I don't have data on that right now. Try asking me about KLE Tech's programs, placement statistics, or fee structure!",
    "I'm not sure about that one. My knowledge covers KLE Tech's academic programs, placement records, fee details, and campus info. Feel free to ask about any of those!",
]

def load_retrieval_system(dataset_path="kle_tech_dataset.jsonl"):
    """Loads the knowledge base and encodes all questions using Sentence-BERT."""
    knowledge_base = {}
    known_questions = []

    if os.path.exists(dataset_path):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                q = data["user"]
                knowledge_base[q] = data["assistant"]
                known_questions.append(q)

    if not known_questions:
        print(f"Warning: No knowledge found in {dataset_path}")
        return {}, [], None, None

    # Load Sentence-BERT on CPU
    print("Loading Sentence-BERT (all-MiniLM-L6-v2) on CPU...")
    st_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

    # Encode all known questions into dense vectors
    print(f"Encoding {len(known_questions)} questions...")
    question_embeddings = st_model.encode(known_questions, convert_to_tensor=True, show_progress_bar=False)

    return knowledge_base, known_questions, question_embeddings, st_model

def find_best_answer(query, knowledge_base, known_questions, question_embeddings, st_model, k=3, min_score=0.35):
    """Finds the top matching facts using Sentence-BERT cosine similarity."""
    if not known_questions or question_embeddings is None or st_model is None:
        return 0.0, "No knowledge base loaded."

    # Encode the user query
    query_embedding = st_model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity against all stored question embeddings
    cos_scores = util.cos_sim(query_embedding, question_embeddings)[0]

    # Get top-k indices sorted by score descending
    top_results = torch.topk(cos_scores, k=min(k, len(known_questions)))

    # Filter by minimum score threshold
    reliable_hits = []
    for score, idx in zip(top_results.values, top_results.indices):
        if score.item() >= min_score:
            reliable_hits.append({
                "score": score.item(),
                "question": known_questions[idx.item()]
            })

    if not reliable_hits:
        return 0.0, "No highly relevant university data found."

    # Context Purity: if top hit is very strong (>0.7), only use that one
    if reliable_hits[0]["score"] > 0.7:
        reliable_hits = [reliable_hits[0]]

    # Aggregate unique answers
    unique_answers = []
    max_score = reliable_hits[0]["score"]

    for hit in reliable_hits:
        ans = knowledge_base.get(hit["question"])
        if ans and ans not in unique_answers:
            unique_answers.append(ans)

    context_blocks = []
    for i, ans in enumerate(unique_answers):
        context_blocks.append(f"[VERIFIED KNOWLEDGE #{i+1}]: {ans}")

    aggregated_context = "\n".join(context_blocks)
    return max_score, aggregated_context
