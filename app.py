import os
import time
from dotenv import load_dotenv
load_dotenv()  # Load biến từ file .env
import joblib
import pandas as pd
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

# -----------------------------------------------------------------------------
# 1. UI/UX CONFIGURATION & PREMIUM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TrustBite - Thám Tử AI Phân Tích Review Quán Ăn",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Custom button styling for 'Quét Ngay' */
    div.stButton > button {
        background: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        width: 100% !important;
        margin-top: 15px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6) !important;
        background: linear-gradient(135deg, #FF7043 0%, #FFAB91 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Card styling for reviews and metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Styled container for the flagged reviews */
    .review-card {
        background: #1E1E24;
        border-left: 5px solid #FF5722;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOAD DATA AND MODELS WITH STREAMLIT CACHING
# -----------------------------------------------------------------------------
# Paths to assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "reviews_ha_noi_output.csv")
MODEL_PATH = os.path.join(BASE_DIR, "random_forest_seeding.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "metadata_scaler.pkl")

@st.cache_resource
def load_sbert_model():
    """Load Vietnamese SBERT SentenceTransformer model."""
    return SentenceTransformer('keepitreal/vietnamese-sbert')

@st.cache_resource
def load_ml_pipeline():
    """Load trained RandomForest model and StandardScaler using joblib."""
    rf_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return rf_model, scaler

@st.cache_data
def load_and_predict_dataset():
    """
    Load reviews from CSV and pre-compute predictions for all records.
    Precompute SBERT + scaling + RandomForest. Cached to make selection instant.
    """
    df = pd.read_csv(CSV_PATH)
    
    # Load model and encoders inside the cached loader
    rf_model, scaler = load_ml_pipeline()
    sbert = load_sbert_model()
    
    # Pre-process text features
    texts = df['review_text'].fillna("").tolist()
    embeddings = sbert.encode(texts, batch_size=64, show_progress_bar=False)
    
    # Pre-process numerical features
    numeric_features = np.stack([
        df['review_rating'].values, 
        df['reviewer_total_reviews'].values
    ], axis=1)
    scaled_numeric = scaler.transform(numeric_features)
    
    # Concatenate features [text, numeric] to match Combo A structure
    features = np.hstack([embeddings, scaled_numeric])
    
    # Predict seeding flags and probabilities
    df['is_fake'] = rf_model.predict(features)
    df['fake_prob'] = rf_model.predict_proba(features)[:, 1]
    
    return df

# Initialize models and data
with st.spinner("🕵️‍♂️ Đang nạp cơ sở dữ liệu thám tử và AI... Vui lòng đợi trong giây lát!"):
    try:
        # Load and pre-compute the predictions (runs once on startup)
        df_all = load_and_predict_dataset()
    except Exception as e:
        st.error(f"Lỗi khi tải mô hình hoặc dữ liệu: {e}")
        st.stop()

# Get the list of unique restaurants
restaurant_list = sorted(df_all['restaurant_name'].unique().tolist())

# -----------------------------------------------------------------------------
# 3. LLM AGENT INTEGRATION (WITH MOCK RESPONSE)
# -----------------------------------------------------------------------------
def call_llm_agent(restaurant_name, fake_ratio, alternative_restaurant=None):
    """
    Simulates or calls an LLM agent with a "funny, witty, foodie detective" persona.
    Includes placeholder templates for OpenAI and Google Gemini APIs.
    """
    
    system_prompt = """Bạn là "Thám tử ẩm thực TrustBite" - một chuyên gia đánh giá quán ăn cực kỳ xéo xắt, hài hước, đa nghi và có đôi mắt cú vọ chuyên vạch trần các chiêu trò seeding (đánh giá ảo).
Nhiệm vụ của bạn là đưa ra lời khuyên cho người dùng dựa trên tên quán ăn, tỷ lệ đánh giá ảo (seeding ratio) và tên quán ăn thay thế đề xuất (nếu có).

Quy tắc ứng xử:
1. Giọng văn hài hước, châm biếm, sử dụng ngôn ngữ trẻ trung, dí dỏm của giới trẻ Việt Nam (ví dụ: "quay xe", "ét ô ét", "seeding lòi mắt", "bánh vẽ", "phong vị", v.v.).
2. Nếu tỷ lệ seeding cao (trên 20%): Phải khuyên khách "quay xe" gấp, châm chọc việc quán thuê đội seeding viết review 5 sao sáo rỗng, và tích cực giới thiệu quán ăn thay thế đề xuất để cứu rỗi chiếc bụng đói của họ.
3. Nếu tỷ lệ seeding thấp (dưới hoặc bằng 20%): Khuyên khách an tâm đi ăn ngon miệng, khen ngợi quán làm ăn chân chính (nhưng vẫn giữ giọng điệu dí dỏm, không quá nghiêm túc).
4. Phản hồi bằng tiếng Việt sinh động, định dạng Markdown rõ ràng, dễ đọc.
"""

    user_prompt = f"""
Thông tin quét quán ăn:
- Quán ăn đang kiểm tra: {restaurant_name}
- Tỷ lệ đánh giá ảo (Seeding): {fake_ratio:.2f}%
- Quán ăn đề xuất thay thế: {alternative_restaurant if alternative_restaurant else 'Không có'}
"""

    # =========================================================================
    # GOOGLE GEMINI 2.5 FLASH API
    # Đọc API key từ file .env (local) hoặc biến môi trường (production)
    # =========================================================================
    API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY", "")

    def _mock_response():
        """Phản hồi dự phòng khi API lỗi."""
        if fake_ratio > 20:
            return f"""### 🕵️‍♂️ LỜI KHUYÊN TỪ THÁM TỬ: **QUAY XE GẤP!!!** 🚨

Trời đất cản ngăn ơi! **{fake_ratio:.1f}%** review ảo? Quán này không phải đang bán đồ ăn nữa rồi, họ đang bán "bánh vẽ" và bán "content" đó!

Tôi đã soi kỹ các review bị cắm cờ, toàn kiểu văn mẫu ngọt ngào đến sâu răng lặp đi lặp lại như đĩa vỡ. Seeding lộ liễu thế này mà cũng duyệt được, tôi đánh giá tổ biên kịch seeding này 1 điểm về chỗ!

**Lời khuyên:** Đừng để các Tiktoker dắt mũi nữa bạn ơi! Hãy quay xe ngay lập tức trước khi chiếc ví và chiếc dạ dày phải khóc thét.

👉 **Gợi ý quán thay thế cực tín:** Hãy chuyển sang **{alternative_restaurant}** liền! Tỷ lệ đánh giá ảo cực thấp, khách ăn thật, bình luận thật.
"""
        else:
            return f"""### 🕵️‍♂️ LỜI KHUYÊN TỪ THÁM TỬ: **MÚC NGAY CHỜ CHI!** 🟢

A ha! Quán **{restaurant_name}** này vượt qua bài kiểm tra cực kỳ thuyết phục! Tỷ lệ seeding chỉ vỏn vẹn **{fake_ratio:.1f}%** (nằm sâu dưới ngưỡng an toàn 20%).

Hầu hết đánh giá đều là người dùng thật, khen có khen, chê có chê — đó chính là tấm chứng chỉ uy tín của quán làm ăn chân chính.

**Lời khuyên:** Lên đồ, dắt xe ra và đi ăn ngay thôi bạn ơi! Chúc bạn bữa ăn ngon miệng và không bị "hố" nhé! 🍜✨
"""

    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt
        )
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as err:
        return f"⚠️ **Lỗi Gemini API:** `{err}`\n\n---\n\n" + _mock_response()

# -----------------------------------------------------------------------------
# 4. INITIAL INTERFACE & SIDEBAR INPUTS
# -----------------------------------------------------------------------------
# Header Banner
st.markdown("""
<div style="text-align: center; padding: 25px 0; background: linear-gradient(135deg, #1A1D24, #2D323F); border-radius: 16px; margin-bottom: 25px; border: 1px solid rgba(255, 255, 255, 0.08);">
    <h1 style="color: #ECEFF4; font-size: 2.8rem; font-weight: 800; margin-bottom: 5px; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">🕵️‍♂️ TrustBite</h1>
    <h3 style="color: #88C0D0; font-weight: 400; margin-top: 0; font-size: 1.3rem;">Thám Tử AI Phân Tích Review Quán Ăn</h3>
    <p style="color: #D8DEE9; max-width: 650px; margin: 12px auto 0 auto; font-size: 0.95rem; line-height: 1.5;">
        Bạn băn khoăn liệu một quán ăn đang "hot hit" trên TikTok là ngon thật hay do thuê đội ngũ <b>seeding đánh giá ảo 5 sao</b>? 
        Hãy để TrustBite sử dụng mô hình Machine Learning kết hợp LLM Agent vạch trần sự thật!
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar setup
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/detective.png", width=120)
    st.markdown("### ⚙️ Cấu Hình Thám Tử")
    
    # Dropdown selectbox for restaurant names
    selected_restaurant = st.selectbox(
        "Chọn quán ăn cần quét:",
        options=restaurant_list,
        index=0,
        help="Danh sách các quán ăn lấy trực tiếp từ cơ sở dữ liệu reviews."
    )
    
    # Sensitivity threshold slider
    threshold = st.slider(
        "Ngưỡng cảnh báo Seeding (%)",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Nếu tỷ lệ review ảo lớn hơn ngưỡng này, hệ thống sẽ đề xuất quay xe và đổi quán."
    )
    
    # Informative guide
    st.info(
        "💡 **Cách hoạt động:** Mô hình Random Forest sẽ kết hợp Vector SBERT từ review text "
        "cùng với số sao (rating) và số lượng review của tài khoản để phát hiện seeding trong tích tắc."
    )

st.markdown("---")

# Initialize Session State
if 'scanned_restaurant' not in st.session_state:
    st.session_state.scanned_restaurant = None
if 'scanned_time' not in st.session_state:
    st.session_state.scanned_time = 0.0

# Submit Button Container
col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])
with col_btn_2:
    scan_clicked = st.button("🚀 Thám Tử AI, Quét Ngay!")

if scan_clicked:
    st.session_state.scanned_restaurant = selected_restaurant
    st.session_state.scanned_time = time.time()

# -----------------------------------------------------------------------------
# 5. ML PROCESSING AND SUGGESTION LOGIC
# -----------------------------------------------------------------------------
if st.session_state.scanned_restaurant is not None:
    # Filter records for selected restaurant
    df_restaurant = df_all[df_all['restaurant_name'] == st.session_state.scanned_restaurant]
    total_reviews = len(df_restaurant)
    
    # Simulated Scanning Animation (for premium user experience)
    scan_container = st.empty()
    with scan_container.container():
        st.markdown(f"#### 🔍 Đang tiến hành phân tích quán: **{st.session_state.scanned_restaurant}**")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        animations = [
            ("🕵️‍♂️ Đang trích xuất dữ liệu review...", 20),
            ("🧠 Chạy mô hình SBERT mã hóa văn bản tiếng Việt...", 50),
            ("📊 Chuẩn hóa dữ liệu rating và độ uy tín của reviewer...", 80),
            ("🎯 Đưa vào Random Forest để phân loại review ảo/thật...", 100)
        ]
        
        for text, percentage in animations:
            status_text.text(text)
            progress_bar.progress(percentage)
            time.sleep(0.25)
            
        scan_container.empty() # Clear animation once done

    # ML Metrics Calculation
    fake_count = int(df_restaurant['is_fake'].sum())
    fake_ratio = (fake_count / total_reviews) * 100 if total_reviews > 0 else 0
    
    # -------------------------------------------------------------------------
    # 4. ALTERNATIVE SUGGESTION LOGIC
    # -------------------------------------------------------------------------
    alternative_restaurant = None
    if fake_ratio > threshold:
        # Calculate fake ratios for all other restaurants
        other_restaurants = df_all[df_all['restaurant_name'] != st.session_state.scanned_restaurant]
        other_stats = other_restaurants.groupby('restaurant_name').agg(
            total_reviews=('is_fake', 'count'),
            fake_count=('is_fake', 'sum')
        )
        other_stats['fake_ratio'] = (other_stats['fake_count'] / other_stats['total_reviews']) * 100
        
        # Filter for candidates with fake_ratio < 15% and sort by ratio ascending
        candidates = other_stats[other_stats['fake_ratio'] < 15].sort_values(by='fake_ratio')
        
        if not candidates.empty:
            # Pick the restaurant with the absolute lowest fake ratio
            alternative_restaurant = candidates.index[0]
        else:
            # Fallback to the overall minimum fake ratio if none is under 15%
            alternative_restaurant = other_stats.sort_values(by='fake_ratio').index[0]

    # Get advice from LLM Agent
    llm_advice = call_llm_agent(st.session_state.scanned_restaurant, fake_ratio, alternative_restaurant)

    # -----------------------------------------------------------------------------
    # 6. RESULTS UI DISPLAY
    # -----------------------------------------------------------------------------
    st.markdown(f"### 📊 Kết Quả Quét Thám Tử: **{st.session_state.scanned_restaurant}**")
    
    col_results_1, col_results_2 = st.columns([1, 1.5], gap="large")
    
    # LEFT COLUMN: METRICS
    with col_results_1:
        st.markdown("#### 🎯 Chỉ Số Review")
        
        # Metrics using custom cards or Streamlit metrics
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Tổng số đánh giá", value=total_reviews)
        with col_m2:
            st.metric(label="Đánh giá ảo (Seeding)", value=fake_count, delta=f"+{fake_count}", delta_color="inverse")
        with col_m3:
            # Metric for fake ratio with red color warning if exceeds threshold
            st.metric(
                label="Tỷ lệ đánh giá ảo", 
                value=f"{fake_ratio:.1f}%",
                delta=f"Ngưỡng: {threshold}%",
                delta_color="inverse" if fake_ratio > threshold else "normal"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional visual charts / alerts
        if fake_ratio > threshold:
            st.error(
                f"🚨 **CẢNH BÁO:** Tỷ lệ đánh giá ảo vượt quá mức cho phép ({fake_ratio:.1f}% > {threshold}%). "
                f"Nhiều khả năng quán ăn này đang sử dụng dịch vụ chạy seeding đánh giá 5 sao ảo!"
            )
        else:
            st.success(
                f"✅ **AN TOÀN:** Tỷ lệ đánh giá ảo nằm trong mức chấp nhận được ({fake_ratio:.1f}% <= {threshold}%). "
                f"Quán ăn này có lượng review tự nhiên đáng tin cậy."
            )
            
        # Display Pie Chart of Real vs Fake
        chart_data = pd.DataFrame({
            "Loại đánh giá": ["Review Thật (Real)", "Review Ảo (Fake/Seeding)"],
            "Số lượng": [total_reviews - fake_count, fake_count]
        })
        st.write("")
        st.write("**Biểu đồ phân bổ đánh giá:**")
        st.bar_chart(chart_data.set_index("Loại đánh giá"))

    # RIGHT COLUMN: LLM ADVICE
    with col_results_2:
        st.markdown("#### 💬 Lời Khuyên Của Thám Tử AI (LLM Agent)")
        if fake_ratio > threshold:
            st.warning(llm_advice)
        else:
            st.info(llm_advice)

    st.markdown("---")

    # EVIDENCE EXPANDER (SHOWING 3-5 FLAG-SEEDED REVIEWS)
    st.markdown("### 🔍 Phân Tích Bằng Chứng Đánh Giá Ảo")
    with st.expander("📂 Xem Danh Sách Các Đánh Giá Bị Mô Hình Cắm Cờ Nghi Vấn (Top 5)", expanded=True):
        fake_reviews = df_restaurant[df_restaurant['is_fake'] == 1].sort_values(by='fake_prob', ascending=False)
        
        if len(fake_reviews) > 0:
            st.markdown(
                f"Tìm thấy **{len(fake_reviews)}** đánh giá bị cắm cờ seeding. "
                "Dưới đây là 5 đánh giá có độ nghi vấn cao nhất được sắp xếp giảm dần:"
            )
            
            for index, row in fake_reviews.head(5).iterrows():
                st.markdown(f"""
                <div class="review-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem;">
                        <span style="font-weight: 600; color: #FFD54F;">⭐ {row['review_rating']} / 5 Sao</span>
                        <span style="font-size: 0.85em; color: #ECEFF1;">Xác suất ảo: <strong style="color: #FF5722; font-size: 1rem;">{row['fake_prob']*100:.1f}%</strong></span>
                    </div>
                    <p style="font-style: italic; color: #ECEFF1; font-size: 0.95rem; margin-bottom: 10px; line-height: 1.4;">
                        "{row['review_text']}"
                    </p>
                    <div style="font-size: 0.8em; color: #B0BEC5; display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
                        <span>Mã User: <code>{row['reviewer_id']}</code></span>
                        <span>Tổng số review đã viết: <strong>{row['reviewer_total_reviews']}</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 Tuyệt vời! Mô hình không phát hiện đánh giá nào có hành vi seeding đáng nghi ngờ.")
else:
    # Initial state (if no scan has been run yet)
    st.info("👈 Hãy chọn một quán ăn ở bảng điều khiển bên trái và nhấn nút **🚀 Thám Tử AI, Quét Ngay!** để bắt đầu phân tích dữ liệu.")
