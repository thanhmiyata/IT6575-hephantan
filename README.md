# 🗄️ Mini Key-Value Store Service (KVSS)
**Bài thực hành Interface trong Hệ thống Phân tán - IT6575**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://python.org)
[![Protocol](https://img.shields.io/badge/Protocol-TCP-green.svg)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](#)

## 📖 Tổng quan

Dự án này thực hiện một **Key-Value Store Service** đơn giản tuân thủ nghiêm ngặt **Interface Specification KV/1.0**. Đây là bài thực hành nhằm hiểu rõ về:

- 🔌 **Interface Design** trong hệ thống phân tán
- 🌐 **Line-based Protocol** over TCP
- 🔄 **Client-Server Architecture**
- 🧪 **Protocol Testing & Validation**
- 📊 **Network Traffic Analysis**

### ✨ Tính năng chính

- ✅ **TCP Server đa luồng** - Hỗ trợ multiple clients đồng thời
- ✅ **In-memory Storage** - Lưu trữ key-value pairs trong RAM
- ✅ **Comprehensive Logging** - Ghi log chi tiết với timestamp
- ✅ **Robust Error Handling** - Xử lý lỗi đầy đủ theo specification
- ✅ **Interactive & Batch Client** - Hỗ trợ cả chế độ tương tác và batch
- ✅ **Automated Testing Suite** - 10 test cases tự động
- ✅ **Manual Testing Tools** - Hướng dẫn test với nc/telnet/Wireshark

## 📁 Cấu trúc project

```
BTL/
├── 📄 kvss_server.py              # KVSS Server implementation (TCP multi-threaded)
├── 📄 kvss_client.py              # KVSS Client (interactive & batch modes)
├── 🧪 test_kvss.py                # Automated test suite (10 test cases)
├── 📋 manual_test_guide.md        # Manual testing guide (nc/telnet/Wireshark)
├── ❓ answers_interface_questions.md  # Interface design Q&A (5 questions)
├── 📊 kvss_server.log             # Server runtime logs (auto-generated)
├── 📚 README.md                   # Project documentation (this file)
├── 📖 btlt_chap1_tongquan_kientruc_vie.pdf  # Course materials
├── 📖 btth_ch1_tongquan_kientruc_vie.pdf   # Lab instructions
└── 🐍 venv/                       # Python virtual environment
    ├── bin/activate               # Virtual environment activation
    └── lib/python3.13/site-packages/  # Dependencies
```

### 📊 Thống kê dự án

| Thành phần | Số dòng code | Tính năng |
|------------|-------------|-----------|
| `kvss_server.py` | ~185 LOC | TCP Server, Protocol Parser, Storage Engine |
| `kvss_client.py` | ~139 LOC | Interactive Client, Batch Mode, CLI |
| `test_kvss.py` | ~169 LOC | Automated Testing, 10 Test Cases |
| **Tổng cộng** | **~493 LOC** | **Complete KVSS Implementation** |

## 🔌 Interface Specification KV/1.0

### 🌐 Connection Parameters
| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| **Protocol** | TCP | Transmission Control Protocol |
| **Host** | `127.0.0.1` | Localhost (loopback interface) |
| **Port** | `5050` | Default KVSS service port |
| **Encoding** | `UTF-8` | Character encoding |
| **Format** | Line-based | Mỗi message kết thúc bằng `\n` |

### 📝 Command Syntax (EBNF)
```ebnf
request     ::= version " " command [ " " args ] "\n"
version     ::= "KV/1.0"
command     ::= "PUT" | "GET" | "DEL" | "STATS" | "QUIT"
args        ::= key [ " " value ]
key         ::= word
value       ::= text
word        ::= [a-zA-Z0-9_]+
text        ::= .+
```

### 🎯 Commands Overview

| Command | Syntax | Purpose | Response |
|---------|--------|---------|----------|
| `PUT` | `KV/1.0 PUT <key> <value>` | Store/Update key-value pair | `201 CREATED` / `200 OK` |
| `GET` | `KV/1.0 GET <key>` | Retrieve value by key | `200 OK <value>` / `404 NOT_FOUND` |
| `DEL` | `KV/1.0 DEL <key>` | Delete key-value pair | `204 NO_CONTENT` / `404 NOT_FOUND` |
| `STATS` | `KV/1.0 STATS` | Get server statistics | `200 OK keys=N uptime=Ns served=N` |
| `QUIT` | `KV/1.0 QUIT` | Close connection | `200 OK bye` |

### 📊 HTTP-style Status Codes

| Code | Status | Meaning | When |
|------|--------|---------|------|
| `200` | `OK [data]` | ✅ Success with optional data | GET success, STATS, QUIT |
| `201` | `CREATED` | ✅ Resource created successfully | PUT new key |
| `204` | `NO_CONTENT` | ✅ Success, no content returned | DEL success |
| `400` | `BAD_REQUEST` | ❌ Invalid syntax/command | Malformed request |
| `404` | `NOT_FOUND` | ❌ Key does not exist | GET/DEL non-existent key |
| `426` | `UPGRADE_REQUIRED` | ❌ Missing/wrong version | No "KV/1.0" prefix |
| `500` | `SERVER_ERROR` | ❌ Internal server error | Unexpected server error |

## 🚀 Quick Start Guide

### 📋 Prerequisites

```bash
# Kiểm tra Python version
python3 --version  # Python 3.6+ required

# Optional: Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Kiểm tra các tools cần thiết cho manual testing
nc -h     # netcat
telnet    # telnet client
wireshark # packet analyzer (optional)
```

### 1️⃣ Khởi động KVSS Server

```bash
# Khởi động server (default: 127.0.0.1:5050)
python3 kvss_server.py

# Output mong đợi:
# 2024-01-15 10:30:00,123 - INFO - KVSS Server đã khởi động tại 127.0.0.1:5050
```

**Server Features:**
- 🔄 **Multi-threaded**: Hỗ trợ multiple clients đồng thời
- 📝 **Auto-logging**: Ghi log vào `kvss_server.log`
- 💾 **In-memory storage**: Dữ liệu lưu trong RAM
- 🛡️ **Error handling**: Xử lý lỗi robust

### 2️⃣ Sử dụng KVSS Client

#### 🎮 Interactive Mode (Chế độ tương tác)
```bash
python3 kvss_client.py

# Giao diện interactive:
# === KVSS Client - Chế độ tương tác ===
# Nhập lệnh theo format: KV/1.0 <COMMAND> [args]
# Ví dụ: KV/1.0 PUT user42 Alice
# Gõ 'exit' để thoát

KVSS> KV/1.0 PUT user42 Alice
Server: 201 CREATED

KVSS> KV/1.0 GET user42  
Server: 200 OK Alice

KVSS> exit
Server: 200 OK bye
```

#### 🤖 Batch Mode (Chế độ test nhanh)
```bash
python3 kvss_client.py --batch

# Chạy pre-defined test commands:
# [1] Client: KV/1.0 PUT user42 Alice
# [1] Server: 201 CREATED
# [2] Client: KV/1.0 GET user42
# [2] Server: 200 OK Alice
# ...
```

#### ⚙️ Custom Host/Port
```bash
python3 kvss_client.py --host 192.168.1.100 --port 8080
```

### 3️⃣ Manual Testing với Netcat

#### Terminal 1 - Server:
```bash
python3 kvss_server.py
```

#### Terminal 2 - Client với netcat:
```bash
# Kết nối tới server
nc 127.0.0.1 5050

# Test commands:
KV/1.0 PUT user42 Alice    # → 201 CREATED
KV/1.0 GET user42          # → 200 OK Alice  
KV/1.0 PUT user42 Bob      # → 200 OK
KV/1.0 STATS               # → 200 OK keys=1 uptime=30s served=4
KV/1.0 DEL user42          # → 204 NO_CONTENT
KV/1.0 GET user42          # → 404 NOT_FOUND
KV/1.0 QUIT                # → 200 OK bye
```

### 4️⃣ Automated Testing Suite

```bash
# Chạy 10 test cases tự động
python3 test_kvss.py

# Output mong đợi:
# === BỘ KIỂM THỬ KVSS - 10 CA KIỂM THỬ ===
# --- Test Case: PUT hợp lệ - tạo mới ---
# ✅ PASS
# ...
# === KẾT QUẢ KIỂM THỬ ===
# Passed: 10/10
# Success Rate: 100.0%
# 🎉 TẤT CẢ TEST CASE ĐỀU PASS!
```

**Test Coverage:**
- ✅ Valid operations (PUT, GET, DEL, STATS, QUIT)
- ❌ Error scenarios (404, 400, 426)
- 🔄 Idempotent operations
- 📊 Statistics tracking

## 💡 Protocol Examples & Use Cases

### 🎯 Basic Operations Flow

```bash
# 1. Tạo mới key-value pair
Client: KV/1.0 PUT user42 Alice
Server: 201 CREATED                    # ✅ New key created

# 2. Truy xuất value
Client: KV/1.0 GET user42
Server: 200 OK Alice                   # ✅ Value retrieved

# 3. Cập nhật existing key
Client: KV/1.0 PUT user42 Bob
Server: 200 OK                         # ✅ Value updated (not 201)

# 4. Kiểm tra thống kê
Client: KV/1.0 STATS
Server: 200 OK keys=1 uptime=45s served=4

# 5. Xóa key
Client: KV/1.0 DEL user42
Server: 204 NO_CONTENT                 # ✅ Key deleted

# 6. Truy xuất key đã xóa
Client: KV/1.0 GET user42
Server: 404 NOT_FOUND                  # ❌ Key not found

# 7. Đóng kết nối
Client: KV/1.0 QUIT
Server: 200 OK bye                     # ✅ Connection closed
```

### 🚨 Error Scenarios

```bash
# Missing version
Client: PUT user43 Charlie
Server: 426 UPGRADE_REQUIRED           # ❌ Version required

# Invalid command  
Client: KV/1.0 POTT user44 David
Server: 400 BAD_REQUEST                # ❌ Unknown command

# Missing arguments
Client: KV/1.0 PUT user45
Server: 400 BAD_REQUEST                # ❌ Value required for PUT

# Non-existent key
Client: KV/1.0 GET nonexistent
Server: 404 NOT_FOUND                  # ❌ Key doesn't exist

# Delete non-existent key (idempotent)
Client: KV/1.0 DEL nonexistent
Server: 404 NOT_FOUND                  # ❌ Key doesn't exist
```

### 🔄 Advanced Use Cases

#### Multi-value Storage
```bash
Client: KV/1.0 PUT config database_url postgresql://localhost:5432/mydb
Server: 201 CREATED

Client: KV/1.0 PUT config max_connections 100
Server: 200 OK

Client: KV/1.0 GET config
Server: 200 OK max_connections 100     # Latest value wins
```

#### Session Management
```bash
Client: KV/1.0 PUT session:user123 {"login_time":"2024-01-15T10:30:00Z","role":"admin"}
Server: 201 CREATED

Client: KV/1.0 GET session:user123
Server: 200 OK {"login_time":"2024-01-15T10:30:00Z","role":"admin"}

Client: KV/1.0 DEL session:user123
Server: 204 NO_CONTENT
```

#### Statistics Monitoring
```bash
Client: KV/1.0 STATS
Server: 200 OK keys=5 uptime=3600s served=150

# Keys: số key hiện tại trong store
# Uptime: thời gian server đã chạy (giây)  
# Served: tổng số requests đã xử lý
```

## 🔍 Network Analysis với Wireshark

### 🎯 Mục đích
- Quan sát **TCP 3-way handshake**
- Phân tích **line-based protocol** 
- Hiểu **packet segmentation**
- Debug connection issues

### 📋 Hướng dẫn nhanh
```bash
# 1. Khởi động Wireshark
sudo wireshark  # Linux
wireshark       # macOS

# 2. Chọn interface: Loopback (lo0/lo)
# 3. Apply filter: tcp.port == 5050
# 4. Start capture

# 5. Test traffic
nc 127.0.0.1 5050
KV/1.0 PUT test_key test_value
KV/1.0 GET test_key
KV/1.0 QUIT

# 6. Analyze: Right-click packet → Follow TCP Stream
```

### 📊 Quan sát được
- **TCP handshake**: SYN → SYN-ACK → ACK
- **Text protocol**: Human-readable commands
- **Line delimiters**: `\n` separators
- **Connection termination**: FIN → ACK → FIN → ACK

**📖 Chi tiết**: Xem `manual_test_guide.md`

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
