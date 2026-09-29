# Thông Tin Deploy — Checkpoint 5

## Thông Tin Học Viên

| Mục | Nội dung |
|---|---|
| Họ và tên | Nguyễn Hồng Cường |
| Mã học viên | 2A202602415 |
| Repo | https://github.com/hongcuong26-debug/K4-L3B-DAY12-NguyenHongCuong-2A202602415-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|---|---|
| URL kiểm tra local | http://localhost:8000 |
| Platform | Local Docker Compose fallback; cấu hình Render và Railway đã chuẩn bị |
| Ngày kiểm tra | 2026-09-29 |

Chưa tạo public cloud service vì phiên làm việc này không có quyền truy cập tài
khoản Railway/Render. Bài dùng phương án local fallback, vì vậy CP5 bị giới hạn
tối đa 9/15 điểm theo rubric. Không có URL hoặc output cloud nào được bịa.

## Biến Môi Trường

Các tên biến cần đặt trên cloud:

- `AGENT_API_KEY`: secret do người dùng tự sinh và lưu trong dashboard.
- `REDIS_URL`: lấy từ Redis add-on của platform.
- `RATE_LIMIT_PER_MINUTE`: cấu hình giới hạn request.
- `MONTHLY_BUDGET_USD`: cấu hình ngân sách tháng.
- `LOG_LEVEL`: mức log.
- `PORT`: do platform tự cấp.

Tài liệu này không chứa giá trị của bất kỳ secret nào.

## Kết Quả Chạy Thật Với Docker Compose

```text
agent: Up (healthy), 0.0.0.0:8000->8000/tcp
redis: Up (healthy), 0.0.0.0:6379->6379/tcp

GET /health
200 {"status":"ok","service":"day12-agent","version":"1.0.0"}

GET /ready
200 {"status":"ready","redis":true}

POST /ask không có X-API-Key
401 Unauthorized

POST /ask có X-API-Key và X-User-Id: sv01
200; user_id=sv01; history_length=0; answer_present=true
```

Image production đã build thành công:

```text
day12-agent:prod
size_bytes=63855176
user=app
```

Ảnh endpoint thật nằm tại `screenshots/health.png`. Ảnh dashboard cloud chưa có
vì chưa triển khai lên tài khoản cloud.
