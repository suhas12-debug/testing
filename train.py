import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim
import math
import random
import os

from vocab_builder import VocabBuilder, load_and_preprocess_data, save_vocab, PAD_token, SOS_token, EOS_token
from transformer_model import Seq2SeqTransformer, create_mask

# Hyperparameters
EMB_SIZE = 128
NHEAD = 4
FFN_HID_DIM = 256
BATCH_SIZE = 8
NUM_ENCODER_LAYERS = 2
NUM_DECODER_LAYERS = 2
NUM_EPOCHS = 200
LEARNING_RATE = 0.0005

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ChatDataset(Dataset):
    def __init__(self, pairs, vocab):
        self.pairs = pairs
        self.vocab = vocab

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        pair = self.pairs[idx]
        src = self.vocab.sentence_to_indices(pair["user"])
        tgt = self.vocab.sentence_to_indices(pair["assistant"])
        return src, tgt

def collate_fn(batch):
    src_batch, tgt_batch = [], []
    for src_item, tgt_item in batch:
        src_batch.append(torch.tensor([SOS_token] + src_item + [EOS_token]))
        tgt_batch.append(torch.tensor([SOS_token] + tgt_item + [EOS_token]))
        
    src_batch = nn.utils.rnn.pad_sequence(src_batch, padding_value=PAD_token)
    tgt_batch = nn.utils.rnn.pad_sequence(tgt_batch, padding_value=PAD_token)
    return src_batch, tgt_batch

def train_epoch(model, optimizer, criterion, dataloader):
    model.train()
    losses = 0
    for src, tgt in dataloader:
        src = src.to(DEVICE)
        tgt = tgt.to(DEVICE)

        # tgt_input is the input to the decoder (shifted right, omitting the last EOS)
        tgt_input = tgt[:-1, :]
        tgt_mask, tgt_mask_square, src_padding_mask, tgt_padding_mask = create_mask(src, tgt_input, PAD_token)
        
        # moving masks to device
        tgt_mask_square = tgt_mask_square.to(DEVICE)
        src_padding_mask = src_padding_mask.to(DEVICE)
        tgt_padding_mask = tgt_padding_mask.to(DEVICE)
        tgt_mask = tgt_mask.to(DEVICE)

        logits = model(src, tgt_input, tgt_mask, tgt_mask_square, src_padding_mask, tgt_padding_mask, src_padding_mask)
        
        optimizer.zero_grad()
        # tgt_out is what we try to predict (shifted left, omitting the SOS)
        tgt_out = tgt[1:, :]
        
        loss = criterion(logits.reshape(-1, logits.shape[-1]), tgt_out.reshape(-1))
        loss.backward()
        optimizer.step()
        losses += loss.item()
        
    return losses / len(dataloader)

def main():
    print(f"Using device: {DEVICE}")
    
    # 1. Load Data and Vocabulary
    vocab = VocabBuilder("KLETech")
    # True to use our synonym data augmentation
    pairs = load_and_preprocess_data("kle_tech_dataset.jsonl", vocab, augment=True, num_augments=5)
    
    # Check if dataset is loaded
    if len(pairs) == 0:
        print("Dataset is empty. Exiting.")
        return
        
    save_vocab(vocab, "vocab.json")
    print(f"Vocabulary saved, size: {vocab.num_words}")
    
    # 2. Prepare DataLoader
    dataset = ChatDataset(pairs, vocab)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    
    # 3. Define Model
    model = Seq2SeqTransformer(
        num_encoder_layers=NUM_ENCODER_LAYERS,
        num_decoder_layers=NUM_DECODER_LAYERS,
        emb_size=EMB_SIZE,
        nhead=NHEAD,
        src_vocab_size=vocab.num_words,
        tgt_vocab_size=vocab.num_words,
        dim_feedforward=FFN_HID_DIM
    ).to(DEVICE)
    
    for p in model.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)
            
    criterion = nn.CrossEntropyLoss(ignore_index=PAD_token)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, betas=(0.9, 0.98), eps=1e-9)
    
    # 4. Train Loop
    print("\nStarting Training...")
    best_loss = float('inf')
    
    for epoch in range(1, NUM_EPOCHS + 1):
        loss = train_epoch(model, optimizer, criterion, dataloader)
        if epoch % 10 == 0 or epoch == 1:
            print(f"Epoch {epoch}/{NUM_EPOCHS}, Loss: {loss:.4f}")
            
        # Simplistic "save best" logic over the train set since we lack validation set here
        if loss < best_loss:
            best_loss = loss
            torch.save(model.state_dict(), "kle_tech_bot.pth")
            
    print(f"Training Complete! Best Loss: {best_loss:.4f}. Model saved as 'kle_tech_bot.pth'")

if __name__ == "__main__":
    main()
