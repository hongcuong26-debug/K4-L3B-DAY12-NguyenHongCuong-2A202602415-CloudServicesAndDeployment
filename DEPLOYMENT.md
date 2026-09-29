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
| Public URL | https://day12-agent-pmpw.onrender.com |
| Platform | Render Blueprint |
| Ngày kiểm tra | 2026-09-29 |

Render Blueprint `day12-agent-cuong` đã tạo:

- Web service: `day12-agent`
- Key Value/Redis: `day12-redis`
- Branch: `main`
- Commit deploy: `64d23e9` (`CP3`)

## Biến Môi Trường

Các tên biến đã đặt trên Render:

- `AGENT_API_KEY`: secret do người dùng tự sinh và lưu trong dashboard.
- `REDIS_URL`: lấy từ Render Key Value `day12-redis`.
- `RATE_LIMIT_PER_MINUTE`: `10`.
- `MONTHLY_BUDGET_USD`: `10.0`.
- `LOG_LEVEL`: `INFO`.
- `PORT`: do platform tự cấp.

Tài liệu này không chứa giá trị của bất kỳ secret nào.

## Kết Quả Kiểm Tra Cloud

```text
curl -i https://day12-agent-pmpw.onrender.com/health
HTTP/1.1 200 OK
{"status":"ok","service":"day12-agent","version":"1.0.0"}

curl -i https://day12-agent-pmpw.onrender.com/ready
HTTP/1.1 200 OK
{"status":"ready","redis":true}

POST https://day12-agent-pmpw.onrender.com/ask không có X-API-Key
HTTP/1.1 401 Unauthorized
{"detail":"invalid or missing API key"}
```

Image production đã build thành công:

```text
day12-agent:prod
size_bytes=63855176
user=app
```

Ảnh endpoint thật nằm tại `screenshots/health.png`. Ảnh dashboard Render cần
lưu tại `screenshots/dashboard.png`.
