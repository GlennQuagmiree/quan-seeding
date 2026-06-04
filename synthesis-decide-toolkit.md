# Toolkit — Từ Evidence Đến Build Slice
*Dùng sau khi nhóm đã có evidence. Mục tiêu là chốt một build slice đủ nhỏ cho Day 06.*

---

## 1. Gom evidence thành cụm

*Gom theo workflow/pain, không gom theo tên feature.*

**Cụm 1 — "Không biết đang bị lừa"**
- ~70% người dùng gặp quán 4.8–5.0 sao nhưng chất lượng thực tế tệ
- Review 5 sao không còn là tín hiệu đáng tin — người dùng mất công cụ định hướng
- Dịch vụ seeding rao bán công khai 2.000–5.000đ/review, gói 100 review chỉ 300.000đ

**Cụm 2 — "Kiểm tra thủ công tốn thời gian mà vẫn không chắc"**
- Đa số mất >5 phút đọc review trước khi đặt
- Phải hỏi bạn bè, đối chiếu hình ảnh, đọc review 1 sao — không có quy trình chuẩn
- Sau khi bị lừa: "bực mình", "không muốn dùng app nữa" — pain đủ sâu để thay đổi hành vi

**Cụm 3 — "Muốn biết lý do, không muốn AI tự quyết thay"**
- >60% chọn AI hiển thị cảnh báo để tự quyết (Recall), không muốn AI tự động ẩn review
- Bằng chứng tin AI nhất: review trùng nhau + bất thường thời gian đăng + tài khoản ảo
- Lo ngại false positive: "có thể gây thiệt hại kinh tế cho chủ quán"

---

## 2. Viết insight

**Form:**
> User [segment] không chỉ gặp [surface need].  
> Họ thật ra cần [deeper need].  
> Vì [evidence pattern].

**Insight của TrustBite:**

> Người dùng đặt đồ ăn online không chỉ cần biết "quán này có ngon không".  
> Họ thật ra cần **công cụ xác minh quyết định** — một lớp tin tưởng thứ hai giúp họ biết liệu rating 5 sao có đáng tin không, trước khi bỏ tiền.  
> Vì 70% đã từng bị lừa, tốn >5 phút kiểm tra thủ công mỗi lần, và cảm xúc sau khi sai là mất niềm tin vào cả nền tảng — không chỉ mất tiền bữa đó.

---

## 3. Viết opportunity

**Form:**
> Cơ hội là dùng AI để [augment/automate hành động hẹp],  
> giúp user [kết quả],  
> trong khi vẫn kiểm soát [failure/risk].

**Opportunity của TrustBite:**

> Cơ hội là dùng AI để **phân tích dấu hiệu seeding trong tập review của một quán cụ thể**,  
> giúp người dùng rút ngắn từ 5 phút kiểm tra thủ công xuống còn ~10 giây và ra quyết định với nhiều thông tin hơn,  
> trong khi vẫn để người dùng kiểm soát ngưỡng cảnh báo và tự đọc các review bị gắn cờ để phán đoán cuối cùng.

---

## 4. Chọn build slice

| Câu hỏi | Đạt khi | TrustBite — Đánh giá |
|---|---|---|
| User cụ thể chưa? | Nói được ai dùng, trong bối cảnh nào | ✅ Người dùng Hà Nội đang phân vân chọn quán tối, vừa được bạn bè giới thiệu một quán |
| Task đủ hẹp chưa? | Demo được trong 3–5 phút | ✅ Chọn quán → bấm "Quét Ngay" → thấy kết quả trong <5 giây |
| AI decision rõ chưa? | AI gợi ý/tự làm một việc cụ thể | ✅ Ensemble ML cho xác suất từng review → LLM Agent đưa lời khuyên có đổi quán không |
| Failure path rõ chưa? | Có một case AI không chắc hoặc sai để test | ✅ Slider ngưỡng 5–50% + top 5 review bị gắn cờ để user tự kiểm tra |
| Có evidence không? | Có bằng chứng từ self-use/review/user/competitor | ✅ 101 responses khảo sát + self-use trên app đang chạy + Fakespot/ReviewMeta |

**Build slice được chọn:**
> Người dùng chọn tên quán (từ DB sẵn hoặc crawl realtime) → Ensemble model (SBERT + RF + TF-IDF + XGBoost) tính xác suất từng review là seeding → Hiển thị tỷ lệ tổng hợp + top 5 review nghi vấn → LLM Agent (Gemini/Claude) đưa lời khuyên có đổi quán không kèm gợi ý thay thế.

---

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định | TrustBite — Áp dụng |
|---|---|---|
| Evidence yếu, user mờ hồ | Dùng build slice; quay lại research 20 phút | Không áp dụng — evidence rõ từ 101 responses |
| Ý tưởng quá rộng | Giữ domain, cắt xuống một flow | ✅ Áp dụng: không build đặt bàn hay gợi ý menu — chỉ một flow kiểm tra seeding |
| AI không cần thiết | Dùng rule/manual prototype; ghi rõ vì sao không dùng AI sau | Không áp dụng — phân tích 100+ review thủ công là bất khả thi cho user |
| Rủi ro cao | Chọn augmentation hoặc conditional automation | ✅ Áp dụng: chọn Augment thay vì tự động ẩn review vì false positive gây hại quán |
| Không demo được trong 1 ngày | Đưa phần lớn vào backlog, giữ một path nhỏ | Không áp dụng — app đang chạy, demo được trong 3–5 phút |

**Quyết định cuối:** **Giữ nguyên scope hiện tại** — build slice đủ hẹp, evidence đủ mạnh, rủi ro đã có cơ chế xử lý.

---

## 6. Câu chốt cuối

> Dựa trên **101 phản hồi khảo sát người dùng thực + self-use trên app đang chạy**,  
> nhóm sẽ build **TrustBite — flow kiểm tra seeding review cho một quán cụ thể**,  
> cho **người dùng đang phân vân chọn quán ăn tối tại Hà Nội**,  
> để giải quyết **nỗi đau mất niềm tin vào hệ thống review sau khi bị lừa bởi rating ảo**,  
> bằng cách AI **phân tích dấu hiệu seeding và highlight review nghi vấn cụ thể** (không tự quyết thay user),  
> và sẽ test failure path **AI gắn cờ nhầm review thật** bằng slider ngưỡng + top 5 review để user tự đối chiếu.

---

## 7. Backlog

*Những thứ không build trong Day 06:*

- **Feedback loop**: Cho phép user đánh dấu "review này thật / ảo" để cải thiện model — cần database lưu trạng thái
- **Badge "Đã xác minh mua hàng"**: 30%+ respondents yêu cầu — cần tích hợp với platform (GrabFood, Shopee Food)
- **Lịch sử thay đổi điểm sao**: Hiển thị timeline rating của quán theo thời gian — cần crawl lịch sử, không làm được trong 1 ngày
- **Hình phạt / báo cáo quán seeding**: Nhiều user yêu cầu cơ chế khiếu nại — ngoài phạm vi prototype
- **Ensemble nâng cao**: Thêm burst timing detection và text similarity clustering như ReviewMeta — roadmap v2

---

*Batch 02 · Day 06 — VinUni AI Thực Chiến · 04/06/2026*
