# Template — Thin SPEC Cuối Day 06
*Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.*

---

## 1. Track, product/app và user

**Track:** Food & Local Delivery (Zone 3)

**Product/app thật:** TrustBite — Thám Tử AI Phân Tích Review Quán Ăn ([localhost:8501](http://localhost:8501))

**User cụ thể:** Người dùng Hà Nội (18–30 tuổi, đặt đồ ăn 2–3 lần/tuần trên Shopee Food / Be Food / Grab Food), đang phân vân chọn quán tối, vừa thấy một quán được giới thiệu có rating 4.8–5.0 sao nhưng chưa biết có đáng tin không.

**Nhóm có phải user thật không?** Có — các thành viên nhóm đều thường xuyên đặt đồ ăn online và đã tự trải nghiệm bị lừa bởi review ảo. Khảo sát 101 responses xác nhận pain này không chỉ của nhóm.

---

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| ~70% người dùng đã gặp quán 4.8–5.0 sao nhưng chất lượng thực tế tệ | Khảo sát Google Form, 101 responses | Rating 5 sao không còn là tín hiệu đáng tin — user mất công cụ định hướng | Build slice phải cung cấp tín hiệu thay thế, không chỉ hiển thị lại rating |
| Đa số mất >5 phút kiểm tra review thủ công; phải hỏi bạn bè hoặc đối chiếu ảnh | Khảo sát Q10, Q11 | Quy trình kiểm tra hiện tại tốn thời gian và không đáng tin | AI phải rút ngắn quy trình này, không thêm bước phức tạp |
| >60% muốn AI hiển thị cảnh báo để tự quyết, không muốn AI tự ẩn review | Khảo sát Q13 | User muốn Augment, không muốn Automate | Chọn Augmentation — user giữ quyền quyết định cuối |
| Bằng chứng tin AI nhất: review trùng nhau + bất thường thời gian đăng + tài khoản mới | Khảo sát Q14 | User cần explainability, không chỉ con số xác suất | Hiển thị top 5 review bị gắn cờ kèm xác suất cụ thể, không chỉ tỷ lệ tổng |
| Cảm xúc sau khi bị lừa: "bực mình", "không muốn dùng app nữa" | Khảo sát Q7 | Pain đủ sâu để thay đổi hành vi — không chỉ mất tiền một bữa | SPEC phải giải quyết vấn đề niềm tin, không chỉ thông tin |
| Dịch vụ seeding rao bán 2.000–5.000đ/review, gói 100 review chỉ 300.000đ | Quan sát trực tiếp từ group Facebook | Supply của review ảo rất rẻ và dễ mua — vấn đề có thật và có hệ thống | Model cần nhận ra cả pattern hành vi (tài khoản mới, rating 5 sao đồng loạt) chứ không chỉ text |

---

## 3. Pain statement

> **Người dùng đặt đồ ăn online** đang gặp khó ở **việc chọn quán lạ dựa trên review Google Maps**,  
> vì **rating 5 sao đã bị thao túng bởi dịch vụ seeding giá rẻ, không phân biệt được bằng mắt thường**,  
> dẫn đến **mất tiền, mất thời gian, và mất niềm tin vào toàn bộ hệ thống review**.  
> Bằng chứng chính là **70% trong 101 khảo sát đã từng bị lừa; cảm xúc sau đó là "không muốn dùng app nữa"**.

---

## 4. Build slice

> Cho **người dùng đang phân vân chọn quán tối**,  
> prototype sẽ dùng AI để **phân tích tập review của một quán cụ thể, tính xác suất từng review là seeding, và highlight top 5 review nghi vấn nhất kèm lý do**,  
> ra **tỷ lệ seeding tổng hợp + lời khuyên từ LLM Agent (có nên đổi quán không)**,  
> và xử lý **failure mode AI gắn cờ nhầm** bằng **slider ngưỡng 5–50% để user tự điều chỉnh + hiển thị xác suất cụ thể thay vì nhãn nhị phân**.

---

## 5. Auto/Aug decision

**Chọn:** ☑ **Augmentation** — AI gợi ý/draft/phân loại, user quyết cuối.

**Lý do chọn:**
- Human role: **decider** — user tự đọc các review bị gắn cờ và quyết định có tin vào quán không
- Hậu quả của sai (false positive) là đáng kể: gắn cờ nhầm một quán ngon làm ăn chân chính → ảnh hưởng uy tín và doanh thu của họ
- 60%+ user trong khảo sát xác nhận họ muốn tự quyết, không muốn AI ẩn review tự động
- Chỉ nâng lên Conditional Automation khi accuracy mô hình vượt 90%+ và có cơ chế khiếu nại cho quán

---

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| **Happy** | Chọn quán có seeding cao (>20%) → banner đỏ cảnh báo hiện ngay → LLM đưa lời khuyên đổi quán + gợi ý quán thay thế có tỷ lệ thấp hơn → top 5 review bị gắn cờ với xác suất cao nhất |
| **Low-confidence** | Chọn quán có tỷ lệ seeding gần ngưỡng (18–22%) → LLM dùng ngôn ngữ dè dặt: "Mô hình phát hiện một số dấu hiệu nghi vấn, hãy đọc kỹ các review bên dưới" → user điều chỉnh slider để xem kết quả thay đổi real-time |
| **Failure** | Nhập tên quán chưa có trong DB → hệ thống kích hoạt crawl Apify realtime (30–60 giây) → quán mới tự động được chọn trong selectbox → phân tích chạy và hiển thị kết quả |
| **Correction** | User không đồng ý với kết quả → kéo slider ngưỡng từ 20% xuống 5% hoặc lên 40% → kết quả cập nhật ngay lập tức, không reload trang → user tự điều chỉnh mức độ nhạy theo phán đoán của mình |

---

## 7. Failure mode nguy hiểm nhất

> Nếu user **chọn một quán ăn ngon, làm ăn chân chính với nhiều review thật ngắn gọn kiểu "Ngon lắm! Sẽ quay lại!"**,  
> AI có thể **gắn cờ nhầm vì các review này có đặc điểm giống seeding: ngắn, cảm thán, tài khoản ít review**,  
> hậu quả là **user bỏ qua một quán ngon, và quán bị đánh giá thấp oan — ảnh hưởng uy tín và doanh thu**.  
> Prototype sẽ xử lý bằng: **hiển thị xác suất 0–100% thay vì nhãn Fake/Real; slider ngưỡng để user tự điều chỉnh; LLM dùng ngôn ngữ "có dấu hiệu nghi vấn" thay vì kết luận tuyệt đối; disclaimer bắt buộc cuối mỗi phản hồi LLM**.  
> Owner kiểm tra path này là: **Đặng Thị Thu Thảo** (safety layer + input validation).

---

## 8. Owner plan cho sáng Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| **Lâm Văn Tài** | Prototype (app.py): UI/UX Streamlit, sidebar, biểu đồ, UX crawl realtime (auto-select) | `app.py` chạy được tại localhost:8501 |
| **Đặng Thị Thu Thảo** | Safety layer: input validation, keyword blocklist, prompt injection guard; hỗ trợ UI/UX | Blocklist hoạt động — nhập "khách sạn" hoặc từ nhạy cảm → bị chặn rõ ràng |
| **Hà Kế Trung Đức** | Model Random Forest + SBERT; precompute embeddings | `models/random_forest_seeding.pkl`, `models/sbert_embeddings.npy` |
| **Nguyễn Đăng Huy** | Model XGBoost + TF-IDF; đánh giá ensemble; kịch bản demo | `models/xgboost_seeding.pkl`, `models/tfidf_vectorizer.pkl`; script demo |
| **Tất cả** | Research / evidence; SPEC; test failure path; chuẩn bị slides | `evidence-pack.md`, `synthesis-decide-toolkit.md`, `thin-spec-template.md`, `reviews_ha_noi_output.csv` |

---

*Batch 02 · Day 06 — VinUni AI Thực Chiến · 04/06/2026*
