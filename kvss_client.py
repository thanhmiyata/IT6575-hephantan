#!/usr/bin/env python3
"""
Mini Key-Value Store Service (KVSS) Client
Tuân thủ Interface Specification KV/1.0
"""

import socket
import sys
import argparse

class KVSSClient:
    def __init__(self, host='127.0.0.1', port=5050):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Kết nối tới KVSS Server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Đã kết nối tới KVSS Server tại {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối"""
        if self.socket:
            self.socket.close()
            print("Đã ngắt kết nối")
    
    def send_request(self, request):
        """Gửi request và nhận response"""
        try:
            # Gửi request
            self.socket.send((request + '\n').encode('utf-8'))
            
            # Nhận response
            response = self.socket.recv(1024).decode('utf-8').strip()
            return response
        except Exception as e:
            print(f"Lỗi gửi/nhận: {e}")
            return None
    
    def interactive_mode(self):
        """Chế độ tương tác - đọc từ stdin"""
        if not self.connect():
            return
        
        print("=== KVSS Client - Chế độ tương tác ===")
        print("Nhập lệnh theo format: KV/1.0 <COMMAND> [args]")
        print("Ví dụ: KV/1.0 PUT user42 Alice")
        print("Gõ 'exit' để thoát")
        print()
        
        try:
            while True:
                try:
                    # Đọc input từ user
                    user_input = input("KVSS> ").strip()
                    
                    if user_input.lower() == 'exit':
                        # Gửi lệnh QUIT trước khi thoát
                        response = self.send_request("KV/1.0 QUIT")
                        if response:
                            print(f"Server: {response}")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Gửi request và in response
                    response = self.send_request(user_input)
                    if response:
                        print(f"Server: {response}")
                    else:
                        print("Không nhận được phản hồi từ server")
                        
                except EOFError:
                    print("\nĐã nhận EOF, thoát...")
                    break
                except KeyboardInterrupt:
                    print("\nĐã nhận Ctrl+C, thoát...")
                    break
                    
        finally:
            self.disconnect()
    
    def batch_mode(self, commands):
        """Chế độ batch - thực thi danh sách lệnh"""
        if not self.connect():
            return
        
        print("=== KVSS Client - Chế độ batch ===")
        
        try:
            for i, command in enumerate(commands, 1):
                print(f"[{i}] Client: {command}")
                response = self.send_request(command)
                if response:
                    print(f"[{i}] Server: {response}")
                else:
                    print(f"[{i}] Không nhận được phản hồi")
                print()
                
        finally:
            self.disconnect()

def main():
    parser = argparse.ArgumentParser(description='KVSS Client')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5050, help='Server port (default: 5050)')
    parser.add_argument('--batch', action='store_true', help='Chế độ batch với các lệnh test')
    
    args = parser.parse_args()
    
    client = KVSSClient(args.host, args.port)
    
    if args.batch:
        # Các lệnh test mẫu
        test_commands = [
            "KV/1.0 PUT user42 Alice",
            "KV/1.0 GET user42",
            "KV/1.0 PUT user43 Bob",
            "KV/1.0 STATS",
            "KV/1.0 DEL user42",
            "KV/1.0 GET user42",
            "KV/1.0 STATS",
            "KV/1.0 QUIT"
        ]
        client.batch_mode(test_commands)
    else:
        client.interactive_mode()

if __name__ == "__main__":
    main()
