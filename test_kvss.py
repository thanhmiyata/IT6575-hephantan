#!/usr/bin/env python3
"""
Bộ test cho Mini Key-Value Store Service (KVSS)
Gồm 10 ca kiểm thử bao gồm cả trường hợp hợp lệ và lỗi
"""

import socket
import time
import threading
import sys
from kvss_server import KVSSServer

class KVSSTestClient:
    def __init__(self, host='127.0.0.1', port=5050):
        self.host = host
        self.port = port
    
    def send_request(self, request):
        """Gửi một request và nhận response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.send((request + '\n').encode('utf-8'))
            response = sock.recv(1024).decode('utf-8').strip()
            sock.close()
            return response
        except Exception as e:
            return f"ERROR: {e}"

def run_test_case(test_name, request, expected_status, client):
    """Chạy một ca kiểm thử"""
    print(f"\n--- Test Case: {test_name} ---")
    print(f"Request: {request}")
    
    response = client.send_request(request)
    print(f"Response: {response}")
    
    # Kiểm tra status code
    if response.startswith(expected_status):
        print("✅ PASS")
        return True
    else:
        print(f"❌ FAIL - Expected: {expected_status}, Got: {response}")
        return False

def main():
    # Khởi động server trong thread riêng
    server = KVSSServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    # Đợi server khởi động
    time.sleep(1)
    
    client = KVSSTestClient()
    passed_tests = 0
    total_tests = 10
    
    print("=== BỘ KIỂM THỬ KVSS - 10 CA KIỂM THỬ ===")
    
    # Test Case 1: PUT hợp lệ - tạo mới
    if run_test_case(
        "PUT hợp lệ - tạo mới", 
        "KV/1.0 PUT user42 Alice", 
        "201 CREATED",
        client
    ):
        passed_tests += 1
    
    # Test Case 2: GET hợp lệ - key tồn tại
    if run_test_case(
        "GET hợp lệ - key tồn tại", 
        "KV/1.0 GET user42", 
        "200 OK Alice",
        client
    ):
        passed_tests += 1
    
    # Test Case 3: PUT hợp lệ - cập nhật
    if run_test_case(
        "PUT hợp lệ - cập nhật", 
        "KV/1.0 PUT user42 Bob", 
        "200 OK",
        client
    ):
        passed_tests += 1
    
    # Test Case 4: DEL hợp lệ - key tồn tại
    if run_test_case(
        "DEL hợp lệ - key tồn tại", 
        "KV/1.0 DEL user42", 
        "204 NO_CONTENT",
        client
    ):
        passed_tests += 1
    
    # Test Case 5: GET lỗi - key không tồn tại
    if run_test_case(
        "GET lỗi - key không tồn tại", 
        "KV/1.0 GET user42", 
        "404 NOT_FOUND",
        client
    ):
        passed_tests += 1
    
    # Test Case 6: DEL lỗi - key không tồn tại (idempotent)
    if run_test_case(
        "DEL lỗi - key không tồn tại", 
        "KV/1.0 DEL user42", 
        "404 NOT_FOUND",
        client
    ):
        passed_tests += 1
    
    # Test Case 7: STATS hợp lệ
    if run_test_case(
        "STATS hợp lệ", 
        "KV/1.0 STATS", 
        "200 OK",
        client
    ):
        passed_tests += 1
    
    # Test Case 8: Lỗi thiếu version
    if run_test_case(
        "Lỗi thiếu version", 
        "PUT user43 Charlie", 
        "426 UPGRADE_REQUIRED",
        client
    ):
        passed_tests += 1
    
    # Test Case 9: Lỗi sai cú pháp - thiếu value cho PUT
    if run_test_case(
        "Lỗi sai cú pháp - thiếu value cho PUT", 
        "KV/1.0 PUT user44", 
        "400 BAD_REQUEST",
        client
    ):
        passed_tests += 1
    
    # Test Case 10: Lệnh không hợp lệ
    if run_test_case(
        "Lệnh không hợp lệ", 
        "KV/1.0 POTT user45 David", 
        "400 BAD_REQUEST",
        client
    ):
        passed_tests += 1
    
    # Tổng kết
    print(f"\n=== KỂT QUẢ KIỂM THỬ ===")
    print(f"Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 TẤT CẢ TEST CASE ĐỀU PASS!")
    else:
        print(f"⚠️  Có {total_tests - passed_tests} test case failed")
    
    # Test QUIT
    print(f"\n--- Test QUIT ---")
    response = client.send_request("KV/1.0 QUIT")
    print(f"QUIT Response: {response}")

if __name__ == "__main__":
    main()
