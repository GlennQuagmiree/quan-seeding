# Template — Evidence Pack
*Nộp kèm thin SPEC cuối Day 06 — Batch 02*

---

## 1. Nhóm và track

**Tên nhóm:** A6  
**Track:** Food & Local Delivery (Zone 3)  
**Product/app đã chọn:** TrustBite — Thám Tử AI Phân Tích Review Quán Ăn  
**Build slice đang nghĩ:** Người dùng nhập tên quán → AI phân tích tỷ lệ review ảo (seeding) → LLM Agent đưa lời khuyên có đổi quán không

---

## 2. Self-use evidence

*Nhóm tự dùng app và ghi lại điểm gãy.*

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Khi chọn quán có tỷ lệ seeding cao (>20%), banner cảnh báo đỏ hiện ngay, LLM gợi ý quán thay thế có tỷ lệ thấp hơn | App chạy tại localhost:8501 | **Happy path** — Ensemble model phân loại đúng, người dùng nhận cảnh báo rõ ràng | Hiển thị xác suất cụ thể (0–100%) thay vì nhãn nhị phân giúp người dùng tự đánh giá dễ hơn |
| Khi nhập tên quán không có trong DB, tính năng crawl Apify realtime hoạt động trong 30–60 giây, quán mới tự động được chọn trong selectbox | App chạy tại localhost:8501 | **Happy path (crawl)** — flow end-to-end từ nhập tên → crawl → phân tích → hiển thị kết quả | Auto-select quán sau crawl giúp UX mượt hơn đáng kể; nếu phải tìm lại thủ công user dễ bỏ cuộc |
| Khi điều chỉnh slider ngưỡng từ 20% → 5%, cùng một quán nhưng đánh giá thay đổi từ "An toàn" sang "Cảnh báo" | App chạy tại localhost:8501 | **Low-confidence path** — AI không chắc, user tự điều chỉnh | Slider real-time là tính năng quan trọng để user kiểm soát độ nhạy của cảnh báo |
| Khi nhập tên khách sạn hoặc từ nhạy cảm, app chặn và hiện thông báo rõ ràng thay vì crash | App chạy tại localhost:8501 | **Failure/Correction** — safety blocklist hoạt động đúng | Validate input trước khi crawl giúp tránh lãng phí Apify credit và bảo vệ uy tín sản phẩm |

---

## 3. User / review / social evidence

*Nguồn: Khảo sát Google Form — 101 responses, thu thập ngày 04/06/2026*

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Bực mình", "không muốn dùng app nữa", "Cảm thấy bị lừa" — cảm xúc phổ biến nhất sau khi đặt quán có review ảo | Khảo sát (101 responses) | Người dùng Shopee Food / Be Food / Grab Food, đặt đồ ăn 2–3 lần/tuần trở lên | Mất niềm tin vào nền tảng sau 1 lần bị lừa — pain sâu hơn việc mất tiền |
| ~70% người trả lời đã từng gặp quán 4.8–5.0 sao nhưng chất lượng thực tế tệ | Khảo sát Q5 | Người dùng thường xuyên đặt đồ ăn online | Review 5 sao không còn là tín hiệu đáng tin; người dùng mất công cụ định hướng |
| Đa số mất trên 5 phút đọc review trước khi đặt; nhiều người phải hỏi bạn bè hoặc đối chiếu hình ảnh thủ công | Khảo sát Q10, Q11 | Tất cả nhóm user | Quy trình kiểm tra review thủ công tốn thời gian và không đáng tin cậy |
| >60% muốn AI hiển thị cảnh báo kèm review để tự quyết định (ưu tiên Recall), không muốn AI tự động ẩn | Khảo sát Q13 | Người dùng quan tâm đến quyền kiểm soát | Người dùng muốn **Augment**, không muốn **Automate** — xác nhận quyết định thiết kế của nhóm |
| Bằng chứng tin tưởng AI nhất: "Trích dẫn review giống hệt nhau" và "phân tích tài khoản ảo / bất thường thời gian đăng" | Khảo sát Q14 | Tất cả | User cần giải thích được (explainability), không chỉ con số xác suất |
| Lo ngại false positive: "Lo ngại vì có thể gây thiệt hại kinh tế cho chủ quán", "Cần minh bạch hóa lý do gắn cờ" | Khảo sát Q15 | ~30% respondents | Failure mode chính của sản phẩm được xác nhận từ phía người dùng thực |

---

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| **Fakespot (Amazon/browser extension)** | Chấm điểm A–F cho từng sản phẩm dựa trên phân tích review; hiển thị badge ngay cạnh rating gốc | Hiển thị kết quả dạng grade + màu sắc giúp user ra quyết định nhanh | ✅ Áp dụng: banner màu đỏ/xanh theo ngưỡng seeding |
| **ReviewMeta** | Phân tích chi tiết pattern review: burst timing, reviewer profile, text similarity | Breakdown theo từng loại dấu hiệu giúp user hiểu AI đang nhìn vào gì | ✅ Áp dụng: top 5 review bị gắn cờ kèm xác suất + lý do |
| **Google Maps "Local Guides"** | Ưu tiên reviewer có lịch sử review nhiều và đa dạng | Hành vi reviewer là tín hiệu mạnh hơn nội dung text | ✅ Áp dụng: 19 features hành vi reviewer trong XGBoost |
| **Yelp Elite / verified purchase** | Badge "Đã mua thật" làm tăng trọng số review | Xác minh giao dịch thực là gold standard cho trust | ❌ Không áp dụng ngay — cần tích hợp với platform |

---

## 5. Evidence → Insight

**Evidence nổi bật nhất:**
- 70% người dùng đã trải nghiệm bị lừa bởi review ảo
- Họ mất 5+ phút kiểm tra thủ công mỗi lần chọn quán
- Cảm xúc sau khi bị lừa: "không muốn dùng app nữa" — tức là pain đủ sâu để thay đổi hành vi

**Insight:**  
User không chỉ gặp vấn đề mất tiền — họ mất **niềm tin vào toàn bộ hệ thống review**. Thật ra họ cần **decision support có thể giải thích được**: không phải AI nói "fake", mà AI chỉ ra *tại sao* nghi vấn và để user tự phán đoán.

**Opportunity:**  
AI có thể giúp bằng cách **augment quy trình đọc review** — thay vì thay thế, TrustBite rút ngắn 5 phút kiểm tra xuống còn 10 giây bằng cách highlight dấu hiệu nghi vấn cụ thể (review trùng nhau, tài khoản mới, burst timing).

---

## 6. Evidence đối SPEC như thế nào?

- [x] Đổi user chính.
- [ ] Đổi pain statement.
- [x] Đổi build slice.
- [ ] Đổi Auto/Aug decision.
- [x] Đổi 4 paths.
- [x] Đổi failure mode.
- [x] Đổi owner/test plan.

**Ghi rõ 1–2 thay đổi quan trọng:**

> **Trước evidence**, nhóm định: Chỉ hiển thị tỷ lệ seeding tổng hợp dạng số %, để AI tự đưa ra verdict "an toàn / không an toàn".
>
> **Sau evidence**, nhóm đổi thành: Hiển thị **xác suất từng review** + top 5 review bị gắn cờ kèm lý do cụ thể; slider ngưỡng để user tự điều chỉnh; LLM dùng ngôn ngữ xác suất ("có dấu hiệu") thay vì kết luận tuyệt đối.
>
> **Lý do:** Khảo sát cho thấy >60% user muốn tự quyết định (Recall > Precision), và lo ngại false positive gây hại cho quán ăn — đòi hỏi explainability cao hơn là accuracy tuyệt đối.

---

*Batch 02 · Day 06 — VinUni AI Thực Chiến · 04/06/2026*
