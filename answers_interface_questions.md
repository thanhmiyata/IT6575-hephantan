# Trả lời 5 câu hỏi về Interface trong Hệ thống Phân tán

## Câu hỏi 1: Interface trong hệ thống phân tán là gì? Tại sao cần phải có Interface khi triển khai các dịch vụ?

### Định nghĩa Interface:
Interface trong hệ thống phân tán là **tập hợp các quy ước chuẩn** mà cả bên cung cấp dịch vụ (server) lẫn bên sử dụng dịch vụ (client) đều phải tuân thủ. Interface quy định:
- Cách thức trao đổi thông điệp
- Cú pháp lệnh và tham số
- Ngữ nghĩa của phản hồi
- Phiên bản của giao thức
- Format dữ liệu và mã hóa

### Tại sao cần Interface:

1. **Tính thống nhất (Consistency)**: Đảm bảo tất cả các thành phần trong hệ thống giao tiếp theo cùng một chuẩn, tránh tình trạng "mạnh ai nấy làm".

2. **Khả năng tương thích (Interoperability)**: Cho phép các hệ thống khác nhau, được phát triển bởi các nhóm khác nhau, có thể tương tác với nhau.

3. **Dễ dàng mở rộng (Scalability)**: Khi có Interface rõ ràng, việc thêm tính năng mới hoặc thay đổi implementation không ảnh hưởng đến các thành phần khác.

4. **Bảo trì và phát triển**: Interface giúp tách biệt implementation khỏi specification, cho phép thay đổi nội bộ mà không ảnh hưởng đến client.

5. **Kiểm thử và debug**: Interface chuẩn giúp việc kiểm thử và debug trở nên dễ dàng hơn.

---

## Câu hỏi 2: Hãy giải thích ý nghĩa của mã trạng thái 201 CREATED, 204 NO_CONTENT và 404 NOT_FOUND trong giao thức KVSS.

### 201 CREATED:
- **Ý nghĩa**: Yêu cầu PUT đã thành công và đã **tạo mới** một key-value pair.
- **Khi nào trả về**: Khi client gửi lệnh `PUT key value` và key này chưa tồn tại trong store.
- **Ví dụ**: 
  ```
  C: KV/1.0 PUT user42 Alice
  S: 201 CREATED  (user42 chưa tồn tại trước đó)
  ```

### 204 NO_CONTENT:
- **Ý nghĩa**: Yêu cầu DEL đã thành công, key đã được xóa, và không có nội dung trả về.
- **Khi nào trả về**: Khi client gửi lệnh `DEL key` và key tồn tại trong store.
- **Ví dụ**:
  ```
  C: KV/1.0 DEL user42
  S: 204 NO_CONTENT  (user42 đã được xóa thành công)
  ```

### 404 NOT_FOUND:
- **Ý nghĩa**: Key được yêu cầu không tồn tại trong store.
- **Khi nào trả về**: 
  - Khi GET một key không tồn tại
  - Khi DEL một key không tồn tại (đảm bảo tính idempotent)
- **Ví dụ**:
  ```
  C: KV/1.0 GET nonexistent_key
  S: 404 NOT_FOUND
  
  C: KV/1.0 DEL nonexistent_key  
  S: 404 NOT_FOUND
  ```

---

## Câu hỏi 3: Trong bài lab KVSS, nếu client không tuân thủ quy ước Interface (ví dụ: thiếu version KV/1.0), server sẽ phản hồi thế nào? Tại sao phải quy định rõ ràng tình huống này?

### Phản hồi của server:
Khi client không tuân thủ Interface (thiếu version KV/1.0), server sẽ trả về:
```
426 UPGRADE_REQUIRED
```

### Ví dụ:
```
C: PUT user42 Alice          (thiếu KV/1.0)
S: 426 UPGRADE_REQUIRED

C: GET user42               (thiếu KV/1.0)  
S: 426 UPGRADE_REQUIRED
```

### Tại sao phải quy định rõ ràng:

1. **Version Control**: Đảm bảo client và server sử dụng cùng phiên bản giao thức. Trong tương lai có thể có KV/2.0 với các tính năng mới.

2. **Backward Compatibility**: Cho phép server hỗ trợ nhiều phiên bản giao thức cùng lúc.

3. **Error Handling**: Client biết chính xác lỗi là gì và cách khắc phục (cập nhật version).

4. **Security**: Ngăn chặn các request không đúng format có thể gây lỗi hoặc tấn công.

5. **Debugging**: Giúp developer dễ dàng xác định nguyên nhân lỗi.

---

## Câu hỏi 4: Quan sát một phiên làm việc qua Wireshark: hãy mô tả cách mà gói tin TCP được chia để truyền thông điệp theo "line-based protocol".

### Cách quan sát với Wireshark:

1. **Khởi động capture**: Chọn interface loopback (lo0/lo), filter `tcp.port == 5050`

2. **Thực hiện test**:
   ```bash
   nc 127.0.0.1 5050
   KV/1.0 PUT user42 Alice
   KV/1.0 GET user42
   ```

### Mô tả quá trình truyền:

#### 1. TCP Connection Setup (3-way handshake):
- **SYN**: Client → Server (thiết lập kết nối)
- **SYN-ACK**: Server → Client (xác nhận + thiết lập ngược)
- **ACK**: Client → Server (hoàn thành handshake)

#### 2. Data Transmission (Line-based Protocol):

**Request từ Client:**
```
TCP Payload: "KV/1.0 PUT user42 Alice\n"
```
- Mỗi dòng lệnh kết thúc bằng `\n` (LF - Line Feed)
- Encoding: UTF-8
- TCP sẽ chia thành các segments nếu dữ liệu lớn

**Response từ Server:**
```
TCP Payload: "201 CREATED\n"
```

#### 3. Đặc điểm Line-based Protocol:

- **Delimiter**: Sử dụng `\n` làm ký tự phân tách giữa các message
- **Human-readable**: Có thể đọc được trong Wireshark's "Follow TCP Stream"
- **Stateless**: Mỗi dòng là một đơn vị độc lập
- **Simple Parsing**: Server chỉ cần đọc đến khi gặp `\n`

#### 4. TCP Segmentation:
- Nếu message nhỏ (< MSS): 1 message = 1 TCP segment
- Nếu message lớn: TCP sẽ chia thành nhiều segments
- Receiver sẽ reassemble các segments theo sequence number

#### 5. Connection Termination:
- **FIN**: Một bên gửi FIN để đóng kết nối
- **ACK**: Bên kia xác nhận
- **FIN**: Bên kia cũng gửi FIN
- **ACK**: Hoàn thành đóng kết nối

---

## Câu hỏi 5: Giả sử có một client viết sai giao thức (gửi KV/1.0 POTT user42 Alice). Server sẽ xử lý như thế nào? Kết quả này thể hiện đặc điểm gì của Interface?

### Xử lý của Server:

Khi nhận được lệnh sai `KV/1.0 POTT user42 Alice`, server sẽ:

1. **Parse request**: Tách thành `["KV/1.0", "POTT", "user42", "Alice"]`
2. **Kiểm tra version**: KV/1.0 ✓ (hợp lệ)
3. **Kiểm tra command**: POTT ❌ (không hợp lệ, không có trong danh sách PUT/GET/DEL/STATS/QUIT)
4. **Trả về lỗi**:
   ```
   400 BAD_REQUEST
   ```

### Ví dụ cụ thể:
```
C: KV/1.0 POTT user42 Alice
S: 400 BAD_REQUEST

C: KV/1.0 PUTT user43 Bob  
S: 400 BAD_REQUEST

C: KV/1.0 GETT user42
S: 400 BAD_REQUEST
```

### Đặc điểm của Interface thể hiện:

#### 1. **Strict Validation (Kiểm tra nghiêm ngặt)**:
- Interface không "đoán" ý định của client
- Mọi sai lệch đều được báo lỗi rõ ràng
- Đảm bảo tính nhất quán trong xử lý

#### 2. **Error Handling (Xử lý lỗi)**:
- Có cơ chế báo lỗi chuẩn (400 BAD_REQUEST)
- Client biết chính xác vấn đề là gì
- Không crash hoặc xử lý sai

#### 3. **Robustness (Tính bền vững)**:
- Server không bị ảnh hưởng bởi input sai
- Tiếp tục hoạt động bình thường sau khi trả lỗi
- Bảo vệ khỏi các lỗi không mong muốn

#### 4. **Predictability (Tính dự đoán được)**:
- Hành vi của server có thể dự đoán trước
- Cùng một input sai sẽ luôn cho cùng một kết quả
- Giúp client debug và khắc phục lỗi

#### 5. **Extensibility (Khả năng mở rộng)**:
- Có thể thêm lệnh mới mà không ảnh hưởng đến logic hiện tại
- Version control cho phép nâng cấp giao thức

### Lợi ích của việc xử lý lỗi nghiêm ngặt:

1. **Phát hiện lỗi sớm**: Tránh để lỗi lan rộng trong hệ thống
2. **Debugging dễ dàng**: Developer biết chính xác lỗi ở đâu
3. **Bảo mật**: Ngăn chặn các cuộc tấn công injection
4. **Reliability**: Hệ thống hoạt động ổn định và đáng tin cậy

---

## Tổng kết

Interface trong hệ thống phân tán là nền tảng quan trọng đảm bảo:
- **Tính thống nhất** trong giao tiếp
- **Khả năng tương thích** giữa các thành phần
- **Tính bền vững** trước các lỗi
- **Khả năng mở rộng** và bảo trì
- **Tính dự đoán được** trong hoạt động

Việc tuân thủ nghiêm ngặt Interface specification là chìa khóa để xây dựng các hệ thống phân tán đáng tin cậy và dễ dàng phát triển.
