# TrustBite - Thám Tử AI Phân Tích Review Quán Ăn 🕵️‍♂️

Ứng dụng Streamlit phát hiện review ảo (seeding) tại các quán ăn Hà Nội sử dụng mô hình **Random Forest** kết hợp **SBERT** (Vietnamese Sentence Transformers) và **LLM Agent (Google Gemini)**.

## 🚀 Tính Năng

- Phát hiện đánh giá ảo (seeding) từ dữ liệu Google Maps reviews
- Mô hình Random Forest + SBERT embedding văn bản tiếng Việt
- LLM Agent (Gemini) đưa ra lời khuyên hài hước, châm biếm
- Giao diện hiện đại, dark mode premium

## ⚙️ Cài Đặt

### 1. Cài thư viện
```bash
pip install streamlit joblib pandas numpy scikit-learn sentence-transformers google-generativeai
```

### 2. Cấu hình API Key Gemini

Tạo file `.streamlit/secrets.toml` (KHÔNG commit file này):
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Hoặc set biến môi trường:
```bash
set GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Chạy ứng dụng
```bash
streamlit run app.py
```

## 📁 Cấu Trúc Project

```
├── app.py                      # Main Streamlit app
├── debug_check.py              # Script kiểm tra dữ liệu
├── random_forest_seeding.pkl   # Mô hình Random Forest đã train
├── metadata_scaler.pkl         # StandardScaler cho metadata
├── reviews_ha_noi_output.csv   # Dataset reviews Hà Nội
└── .streamlit/
    └── config.toml             # Cấu hình Streamlit UI
```

## 🛡️ Lưu Ý Bảo Mật

- **Không** commit `secrets.toml` lên GitHub
- API Key Gemini được đọc từ `st.secrets` (Streamlit Cloud) hoặc biến môi trường
