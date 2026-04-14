import json
import re
import random
import os

PAD_token = 0
SOS_token = 1
EOS_token = 2
UNK_token = 3

class VocabBuilder:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "<PAD>", SOS_token: "<SOS>", EOS_token: "<EOS>", UNK_token: "<UNK>"}
        self.num_words = 4  # Count PAD, SOS, EOS, UNK

        # Simple synonym dictionary for data augmentation (especially for user queries)
        self.synonyms = {
            "what is": ["tell me about", "give me info on", "explain", "describe"],
            "tell me about": ["what is", "can you explain", "give me details about"],
            "how much": ["what is the cost of", "what are the fees for", "give me the price of"],
            "fees": ["cost", "tuition", "price"],
            "placements": ["job opportunities", "recruitment", "hiring", "campus selection"],
            "highest package": ["maximum salary", "top offer", "best package"],
            "average package": ["mean salary", "typical offer"],
            "established": ["founded", "started", "created"],
            "located": ["situated", "placed", "found in"],
            "subjects": ["courses", "curriculum", "syllabus", "topics"],
            "campus": ["college grounds", "university area"],
            "ug courses": ["undergraduate programs", "bachelor degrees"],
        }

    def add_sentence(self, sentence):
        for word in self._tokenize(sentence):
            self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    def _tokenize(self, text):
        # Convert to lowercase and pad punctuation
        text = text.lower()
        text = re.sub(r"([.!?,'()])", r" \1 ", text)
        text = re.sub(r"[^a-zA-Z0-9.!?,'()]+", r" ", text)
        return text.strip().split()

    def augment_sentence(self, sentence):
        """Randomly replace phrases with their synonyms for data augmentation."""
        augmented = sentence.lower()
        
        # Don't augment every single time to keep original data distribution
        if random.random() < 0.3:
            return sentence
            
        for phrase, syn_list in self.synonyms.items():
            if phrase in augmented and random.random() > 0.5:
                # Replace with random synonym
                synonym = random.choice(syn_list)
                # Replace only whole word matches to be safer
                pattern = re.compile(r'\b' + re.escape(phrase) + r'\b')
                augmented = pattern.sub(synonym, augmented, count=1)
                
        # Fix casing for start of string if needed, though we primarily use lowercase
        return augmented.strip()

    def sentence_to_indices(self, sentence):
        tokens = self._tokenize(sentence)
        return [self.word2index.get(word, UNK_token) for word in tokens]

def load_and_preprocess_data(jsonl_file, vocab, augment=True, num_augments=2):
    """
    Loads data from JSONL, builds vocabulary, and returns augmented pairs.
    It returns a list of dictionaries: {"user": ..., "assistant": ...}
    """
    pairs = []
    
    if not os.path.exists(jsonl_file):
        print(f"Warning: File {jsonl_file} not found.")
        return pairs

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                user_msg = data.get("user", "")
                assistant_msg = data.get("assistant", "")
                
                if user_msg and assistant_msg:
                    pairs.append({"user": user_msg, "assistant": assistant_msg})
                    vocab.add_sentence(user_msg)
                    vocab.add_sentence(assistant_msg)
                    
                    # Augment data if enabled
                    if augment:
                        for _ in range(num_augments):
                            aug_user_msg = vocab.augment_sentence(user_msg)
                            # We usually don't augment assistant's response to keep facts intact
                            if aug_user_msg != user_msg.lower():
                                pairs.append({"user": aug_user_msg, "assistant": assistant_msg})
                                vocab.add_sentence(aug_user_msg)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line[:50]}...")

    print(f"Loaded {len(pairs)} turn pairs (including augmentations).")
    print(f"Vocabulary size: {vocab.num_words} words.")
    return pairs

def save_vocab(vocab, filepath):
    data = {
        "word2index": vocab.word2index,
        "index2word": {int(k): v for k, v in vocab.index2word.items()},
        "num_words": vocab.num_words
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_vocab(filepath, name="KLETech"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    vocab = VocabBuilder(name)
    vocab.word2index = data["word2index"]
    vocab.index2word = {int(k): v for k, v in data["index2word"].items()}
    vocab.num_words = data["num_words"]
    return vocab

# Example test run if run directly
if __name__ == "__main__":
    vocab = VocabBuilder("KLETech")
    pairs = load_and_preprocess_data("kle_tech_dataset.jsonl", vocab)
    save_vocab(vocab, "vocab.json")
    
    print("\nSample augmentations:")
    for i in range(min(5, len(pairs))):
        print(f"User: {pairs[i]['user']}")
        print(f"Bot: {pairs[i]['assistant'][:50]}...\n")
