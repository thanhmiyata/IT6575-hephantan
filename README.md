# Mini Key-Value Store Service (KVSS) - Bài thực hành Interface trong Hệ thống Phân tán

## Tổng quan

Đây là bài thực hành về Interface trong các hệ thống phân tán, thông qua việc xây dựng một dịch vụ Mini Key-Value Store Service (KVSS) tuân thủ Interface Specification KV/1.0.

## Cấu trúc project

```
.
├── kvss_server.py              # KVSS Server implementation
├── kvss_client.py              # KVSS Client implementation  
├── test_kvss.py                # Bộ test tự động (10 test cases)
├── manual_test_guide.md        # Hướng dẫn test thủ công với nc/telnet/Wireshark
├── answers_interface_questions.md  # Trả lời 5 câu hỏi về Interface
└── README.md                   # File này
```

## Interface Specification KV/1.0

### Kết nối
- **Protocol**: TCP
- **Default**: 127.0.0.1:5050
- **Encoding**: UTF-8
- **Message format**: Text-based line protocol (kết thúc bằng `\n`)

### Cú pháp lệnh
```
<version> " " <command> [ " " <args> ] "\n"

<version> ::= "KV/1.0"
<command> ::= "PUT" | "GET" | "DEL" | "STATS" | "QUIT"
<args>    ::= <key> [ " " <value> ]
```

### Mã trạng thái
- `200 OK [data]` - Thành công
- `201 CREATED` - Tạo mới thành công (PUT)
- `204 NO_CONTENT` - Xóa thành công (DEL)
- `400 BAD_REQUEST` - Sai cú pháp
- `404 NOT_FOUND` - Key không tồn tại
- `426 UPGRADE_REQUIRED` - Thiếu/sai version
- `500 SERVER_ERROR` - Lỗi server

## Cách sử dụng

### 1. Khởi động Server

```bash
python3 kvss_server.py
```

Server sẽ chạy tại `127.0.0.1:5050` và ghi log vào `kvss_server.log`.

### 2. Sử dụng Client

#### Chế độ interactive:
```bash
python3 kvss_client.py
```

#### Chế độ batch (test nhanh):
```bash
python3 kvss_client.py --batch
```

### 3. Test thủ công với netcat

```bash
# Terminal 1: Khởi động server
python3 kvss_server.py

# Terminal 2: Kết nối với nc
nc 127.0.0.1 5050

# Thực hiện các lệnh:
KV/1.0 PUT user42 Alice
KV/1.0 GET user42
KV/1.0 DEL user42
KV/1.0 STATS
KV/1.0 QUIT
```

### 4. Chạy bộ test tự động

```bash
python3 test_kvss.py
```

Bộ test gồm 10 test cases bao gồm cả trường hợp hợp lệ và lỗi.

## Ví dụ sử dụng

```
Client: KV/1.0 PUT user42 Alice
Server: 201 CREATED

Client: KV/1.0 GET user42  
Server: 200 OK Alice

Client: KV/1.0 PUT user42 Bob
Server: 200 OK

Client: KV/1.0 DEL user42
Server: 204 NO_CONTENT

Client: KV/1.0 GET user42
Server: 404 NOT_FOUND

Client: KV/1.0 STATS
Server: 200 OK keys=0 uptime=12s served=7

Client: KV/1.0 QUIT
Server: 200 OK bye
```

## Test với Wireshark

1. Khởi động Wireshark và chọn interface loopback
2. Áp dụng filter: `tcp.port == 5050`
3. Thực hiện test với nc hoặc client
4. Quan sát TCP packets và line-based protocol

Chi tiết xem trong `manual_test_guide.md`.

## Tính năng

### Server:
- ✅ TCP server đa luồng
- ✅ Lưu trữ key-value trong memory
- ✅ Logging đầy đủ với timestamp
- ✅ Xử lý lỗi robust
- ✅ Idempotent cho GET, STATS, DEL
- ✅ Support multiple clients

### Client:
- ✅ Interactive mode
- ✅ Batch mode  
- ✅ Command line interface
- ✅ Error handling

### Test Coverage:
- ✅ 10 test cases tự động
- ✅ Test cases thủ công với nc/telnet
- ✅ Wireshark packet analysis
- ✅ Error scenarios coverage

## Câu hỏi và trả lời

Xem file `answers_interface_questions.md` để đọc trả lời chi tiết cho 5 câu hỏi về Interface trong hệ thống phân tán:

1. Interface trong hệ thống phân tán là gì?
2. Ý nghĩa các mã trạng thái 201, 204, 404
3. Xử lý khi client không tuân thủ Interface
4. Quan sát line-based protocol qua Wireshark  
5. Xử lý lệnh sai giao thức

## Yêu cầu hệ thống

- Python 3.6+
- Linux/macOS (khuyến nghị Ubuntu)
- Công cụ: netcat, telnet, wireshark (cho test thủ công)

## Lưu ý

- Server sử dụng threading để hỗ trợ multiple clients
- Dữ liệu lưu trong memory (không persistent)
- Log được ghi vào file `kvss_server.log`
- Tuân thủ nghiêm ngặt Interface Specification KV/1.0

## Tác giả

Bài thực hành Interface trong Hệ thống Phân tán - IT6575
