"""
Run once to pre-compute SBERT embeddings for reviews_ha_noi_output.csv.
Saves models/sbert_embeddings.npy so app.py startup is instant.
"""
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

CSV_PATH  = "reviews_ha_noi_output.csv"
OUT_PATH  = "models/sbert_embeddings.npy"

print("Loading CSV...")
df = pd.read_csv(CSV_PATH)
texts = df['review_text'].fillna("").tolist()
print(f"  {len(texts)} reviews")

print("Loading SBERT model...")
sbert = SentenceTransformer('keepitreal/vietnamese-sbert')

print("Encoding (this is the slow part)...")
embeddings = sbert.encode(texts, batch_size=64, show_progress_bar=True)

np.save(OUT_PATH, embeddings)
print(f"Saved to {OUT_PATH} — shape {embeddings.shape}")
