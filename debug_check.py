"""
Debug script - kiểm tra từng bước một
Chạy: python debug_check.py
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"[1] BASE_DIR = {BASE_DIR}")
print(f"[1] Python = {sys.version}")

print("\n[2] Checking required files...")
files = {
    "reviews_ha_noi_output.csv": os.path.join(BASE_DIR, "reviews_ha_noi_output.csv"),
    "random_forest_seeding.pkl": os.path.join(BASE_DIR, "random_forest_seeding.pkl"),
    "metadata_scaler.pkl":       os.path.join(BASE_DIR, "metadata_scaler.pkl"),
}
for name, path in files.items():
    exists = os.path.exists(path)
    size   = os.path.getsize(path) if exists else 0
    print(f"  {'OK' if exists else 'MISSING'} {name} ({size} bytes)")

print("\n[3] Importing pandas / numpy...")
import pandas as pd
import numpy as np
print(f"  pandas {pd.__version__}, numpy {np.__version__}")

print("\n[4] Importing joblib and loading pkl files...")
import joblib
try:
    rf = joblib.load(files["random_forest_seeding.pkl"])
    print(f"  RF model loaded OK: {type(rf)}")
except Exception as e:
    print(f"  ERROR loading RF model: {e}")

try:
    scaler = joblib.load(files["metadata_scaler.pkl"])
    print(f"  Scaler loaded OK: {type(scaler)}")
except Exception as e:
    print(f"  ERROR loading scaler: {e}")

print("\n[5] Loading CSV...")
try:
    df = pd.read_csv(files["reviews_ha_noi_output.csv"])
    print(f"  CSV loaded OK: {df.shape[0]} rows, columns={list(df.columns)}")
except Exception as e:
    print(f"  ERROR loading CSV: {e}")

print("\n[6] Importing sentence_transformers (may take a while)...")
try:
    from sentence_transformers import SentenceTransformer
    print("  SentenceTransformer imported OK")
    print("  Loading model 'keepitreal/vietnamese-sbert' (downloads if not cached)...")
    model = SentenceTransformer('keepitreal/vietnamese-sbert')
    print("  Model loaded OK")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[ALL DONE] If no errors above, the issue is streamlit config or port conflict.")
