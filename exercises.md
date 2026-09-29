# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Các câu trả lời dưới đây dựa trên cấu hình, kết quả chạy
> và quá trình deploy của repo này. Riêng số đo không có sẵn được ghi rõ thay vì
> đoán.
>
> Em trả lời theo những gì đã làm và kiểm tra được trong repo.
>
> Họ và tên: Nguyễn Hồng Cường  Mã học viên: 2A202602415

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi kiểm tra CP1, em từng gặp trường hợp test bỏ `AGENT_API_KEY` nhưng `Settings`
> vẫn khởi tạo được, nên test báo `DID NOT RAISE ValidationError`. Nếu để khóa mặc
> định như `changeme`, app có thể vẫn chạy trên Render mà em không biết dashboard
> đang thiếu secret; người gọi còn có thể dùng khóa công khai đó. Để trường này
> bắt buộc giúp app báo lỗi ngay lúc khởi động, nên em phát hiện và sửa cấu hình
> trước khi đưa service vào sử dụng.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Ví dụ minh họa một dòng theo đúng cấu trúc log của app (timestamp và số liệu
> bên dưới chỉ để minh họa):
>
> ```json
> {"event":"ask_completed","level":"info","timestamp":"2026-09-29T04:20:00+00:00","user_id":"sv01","tokens_in":12,"tokens_out":28,"cost_usd":0.0001}
> ```
>
> Từ các trường này, em có thể lọc những lần gọi của một `user_id` và tính tổng
> `cost_usd` để theo dõi chi phí. Em cũng có thể thống kê số token hoặc đếm số
> sự kiện theo thời gian để tìm lúc service được gọi nhiều. Một dòng `print` chỉ
> nói “đã trả lời xong” thì không có dữ liệu để lọc hay tổng hợp như vậy.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | Em chưa build/lưu số đo bản này nên không ghi số ước đoán |
| Multi-stage | 63.855.176 bytes, khoảng 63,9 MB (60,9 MiB) |

> Em đã xác nhận image production multi-stage có kích thước 63.855.176 bytes.
> Repo hiện không có kết quả build bản một stage để so sánh chính xác. Thông
> thường bản một stage lớn hơn vì image cuối còn giữ cả công cụ và file phục vụ
> quá trình cài dependency; multi-stage chỉ chép dependency đã cài cùng source
> cần chạy sang runtime. Muốn có mức chênh lệch thật, em cần build cả hai trên
> cùng máy và cùng tag/cách đo.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Trong Dockerfile, `requirements.txt` được chép vào builder và dependency được
> cài trước khi source được chép vào runtime. Vì vậy, nếu em chỉ sửa một ký tự
> trong `app/main.py`, các layer cài dependency vẫn dùng lại cache; layer chép
> source và các bước sau nó sẽ chạy lại. Nếu đặt `COPY . .` trước `pip install`,
> thay đổi ở bất kỳ file nào trong source cũng làm layer `COPY` đổi, khiến bước
> cài dependency phía sau phải chạy lại dù `requirements.txt` không đổi.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Nếu app chạy bằng root và có lỗ hổng cho phép kẻ tấn công thực thi lệnh, họ sẽ
> thực thi lệnh với quyền root bên trong container. Nếu tiếp tục khai thác được
> lỗi cấu hình hoặc lỗ hổng thoát container, quyền cao đó có thể làm tăng ảnh
> hưởng lên máy host. `USER app` giới hạn tiến trình từ đầu bằng user thường,
> nên một lỗ hổng trong app không tự động cấp quyền root bên trong container.
> Đây là giảm thiểu rủi ro, chứ không thay thế việc vá lỗi hay cấu hình container
> an toàn.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Với cách đếm theo phút đồng hồ, em có thể gửi 10 request ngay trước thời điểm
> phút đổi, rồi gửi thêm 10 request ngay sau khi bộ đếm reset. Như vậy trong
> khoảng 2 giây bắc qua mốc đó có thể lên tới 20 request. Cửa sổ trượt tính các
> request trong đúng 60 giây gần nhất nên không cho gom hai hạn mức ở hai phút
> liền nhau theo cách này.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit giới hạn tần suất gọi, còn cost guard giới hạn tổng chi phí của một
> user trong tháng UTC. Ví dụ, một user còn quota request nhưng đã gần chạm ngân
> sách và gửi câu hỏi tốn nhiều token: rate limit có thể cho qua, còn cost guard
> sẽ chặn nếu chi phí dự kiến vượt ngân sách. Ngược lại, user mới dùng rất ít
> ngân sách nhưng gửi liên tiếp quá 10 request trong một phút thì cost guard vẫn
> còn cho phép về mặt chi phí, còn rate limit trả `429`.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu cả hai endpoint đều kiểm tra Redis, khi Redis mất kết nối thì cả ba
> container bắt đầu trả `503` cho health check. Orchestrator có thể hiểu nhầm
> dependency đang lỗi là process đã chết, rồi lần lượt restart các container.
> Các container mới vẫn không kết nối được Redis nên tiếp tục unhealthy và bị
> restart, làm cả cụm mất khả năng nhận traffic trong lúc Redis chỉ gián đoạn
> 30 giây. Tách `/health` (chỉ kiểm tra process) khỏi `/ready` (kiểm tra Redis)
> giúp load balancer ngừng gửi request trong thời gian đó mà không cần restart
> app liên tục.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Lịch sử trong bài được lưu ở Redis, nên các instance dùng chung danh sách của
> user và `history_length` không phụ thuộc request trước đó rơi vào container
> nào. Nếu dùng dict Python riêng trong từng process, mỗi container chỉ thấy
> lịch sử mà chính nó đã nhận. Khi request được phân phối sang instance khác,
> `history_length` có thể nhỏ lại hoặc bắt đầu từ 0; sau khi restart container,
> dict đó cũng mất.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Em không ghi nhận lỗi build hoặc health check nào trên Render: service đã lên
> trạng thái Live, `/health` trả `200`, `/ready` trả `200` với `redis: true`, và
> `/ask` không có API key trả `401` như mong đợi. Vì vậy em không muốn ghi một
> thông báo lỗi cloud mà em chưa thực sự gặp. Khi kiểm tra, em đối chiếu URL
> public và trạng thái deploy trên dashboard với các lệnh `curl`; kết quả cho
> thấy cấu hình Redis và cổng do Render cấp đang hoạt động.
