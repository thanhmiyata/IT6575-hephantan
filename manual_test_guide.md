# Hướng dẫn Test thủ công KVSS với nc/telnet và Wireshark

## 1. Chuẩn bị môi trường

### Cài đặt công cụ cần thiết:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install netcat-openbsd telnet wireshark

# macOS
brew install netcat telnet wireshark
```

## 2. Khởi động KVSS Server

```bash
# Khởi động server
python3 kvss_server.py

# Server sẽ chạy tại 127.0.0.1:5050
```

## 3. Test với netcat (nc)

### Terminal 1 - Khởi động server:
```bash
python3 kvss_server.py
```

### Terminal 2 - Test với nc:
```bash
# Kết nối tới server
nc 127.0.0.1 5050

# Sau khi kết nối, gõ các lệnh sau:
KV/1.0 PUT user42 Alice
KV/1.0 GET user42
KV/1.0 PUT user43 Bob
KV/1.0 STATS
KV/1.0 DEL user42
KV/1.0 GET user42
KV/1.0 QUIT
```

### Kết quả mong đợi:
```
201 CREATED
200 OK Alice
201 CREATED
200 OK keys=2 uptime=15s served=4
204 NO_CONTENT
404 NOT_FOUND
200 OK bye
```

## 4. Test với telnet

```bash
# Kết nối tới server
telnet 127.0.0.1 5050

# Thực hiện các lệnh tương tự như nc
```

## 5. Test các trường hợp lỗi

### Test thiếu version:
```bash
nc 127.0.0.1 5050
PUT user44 Charlie
# Expected: 426 UPGRADE_REQUIRED
```

### Test sai cú pháp:
```bash
nc 127.0.0.1 5050
KV/1.0 PUT user45
# Expected: 400 BAD_REQUEST
```

### Test lệnh không hợp lệ:
```bash
nc 127.0.0.1 5050
KV/1.0 POTT user46 David
# Expected: 400 BAD_REQUEST
```

## 6. Quan sát với Wireshark

### Bước 1: Khởi động Wireshark
```bash
sudo wireshark
# hoặc trên macOS: wireshark
```

### Bước 2: Chọn interface
- Chọn interface `Loopback: lo0` (macOS) hoặc `lo` (Linux)
- Bắt đầu capture

### Bước 3: Áp dụng filter
```
tcp.port == 5050
```

### Bước 4: Thực hiện test
```bash
# Terminal khác
nc 127.0.0.1 5050
KV/1.0 PUT test_key test_value
KV/1.0 GET test_key
KV/1.0 QUIT
```

### Bước 5: Phân tích packets
- Tìm các TCP packets với port 5050
- Right-click → Follow → TCP Stream
- Quan sát:
  - TCP 3-way handshake
  - Dữ liệu text-based line protocol
  - TCP connection termination

## 7. Script test tự động

### Chạy bộ test tự động:
```bash
python3 test_kvss.py
```

### Chạy client interactive:
```bash
python3 kvss_client.py
```

### Chạy client batch mode:
```bash
python3 kvss_client.py --batch
```

## 8. Kiểm tra log

Server sẽ ghi log vào file `kvss_server.log`:
```bash
tail -f kvss_server.log
```

## 9. Test đồng thời nhiều client

```bash
# Terminal 1
nc 127.0.0.1 5050

# Terminal 2 (cùng lúc)
nc 127.0.0.1 5050

# Thực hiện các lệnh trên cả 2 terminal để test multi-client
```

## 10. Checklist kiểm thử

- [ ] Server khởi động thành công tại port 5050
- [ ] PUT tạo mới key trả về 201 CREATED
- [ ] PUT cập nhật key trả về 200 OK
- [ ] GET key tồn tại trả về 200 OK + data
- [ ] GET key không tồn tại trả về 404 NOT_FOUND
- [ ] DEL key tồn tại trả về 204 NO_CONTENT
- [ ] DEL key không tồn tại trả về 404 NOT_FOUND (idempotent)
- [ ] STATS trả về 200 OK + thống kê
- [ ] QUIT trả về 200 OK bye
- [ ] Thiếu version trả về 426 UPGRADE_REQUIRED
- [ ] Sai cú pháp trả về 400 BAD_REQUEST
- [ ] Lệnh không hợp lệ trả về 400 BAD_REQUEST
- [ ] Wireshark capture được TCP packets
- [ ] Line-based protocol hiển thị rõ ràng
- [ ] Multiple clients có thể kết nối đồng thời
