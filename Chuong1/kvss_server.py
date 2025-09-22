#!/usr/bin/env python3
"""
Mini Key-Value Store Service (KVSS) Server
Tuân thủ Interface Specification KV/1.0
"""

import socket
import threading
import time
import logging
from datetime import datetime

class KVSSServer:
    def __init__(self, host='127.0.0.1', port=5050):
        self.host = host
        self.port = port
        self.store = {}  # Dictionary lưu trữ key-value
        self.stats = {
            'start_time': time.time(),
            'served_requests': 0
        }
        
        # Thiết lập logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kvss_server.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        """Khởi động server TCP"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.logger.info(f"KVSS Server đã khởi động tại {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f"Kết nối mới từ {client_address}")
                
                # Xử lý client trong thread riêng (có thể dùng single-thread nếu cần)
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            self.logger.error(f"Lỗi khởi động server: {e}")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        """Xử lý một client connection"""
        try:
            while True:
                # Nhận dữ liệu từ client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                # Xử lý từng dòng lệnh
                lines = data.strip().split('\n')
                for line in lines:
                    if line.strip():
                        response = self.process_request(line.strip(), client_address)
                        client_socket.send((response + '\n').encode('utf-8'))
                        
                        # Nếu là lệnh QUIT thì đóng kết nối
                        if line.strip().upper().endswith('QUIT'):
                            break
                            
        except Exception as e:
            self.logger.error(f"Lỗi xử lý client {client_address}: {e}")
        finally:
            client_socket.close()
            self.logger.info(f"Đã đóng kết nối với {client_address}")
    
    def process_request(self, request, client_address):
        """Xử lý một request và trả về response"""
        self.stats['served_requests'] += 1
        self.logger.info(f"Request từ {client_address}: {request}")
        
        try:
            # Parse request theo format: <version> " " <command> [ " " <args> ]
            parts = request.split()
            
            if len(parts) < 2:
                response = "400 BAD_REQUEST"
            elif parts[0] != "KV/1.0":
                response = "426 UPGRADE_REQUIRED"
            else:
                command = parts[1].upper()
                response = self.execute_command(command, parts[2:])
                
        except Exception as e:
            self.logger.error(f"Lỗi xử lý request: {e}")
            response = "500 SERVER_ERROR"
        
        self.logger.info(f"Response tới {client_address}: {response}")
        return response
    
    def execute_command(self, command, args):
        """Thực thi lệnh cụ thể"""
        if command == "PUT":
            return self.handle_put(args)
        elif command == "GET":
            return self.handle_get(args)
        elif command == "DEL":
            return self.handle_del(args)
        elif command == "STATS":
            return self.handle_stats()
        elif command == "QUIT":
            return self.handle_quit()
        else:
            return "400 BAD_REQUEST"
    
    def handle_put(self, args):
        """Xử lý lệnh PUT key value"""
        if len(args) < 2:
            return "400 BAD_REQUEST"
        
        key = args[0]
        value = ' '.join(args[1:])  # Value có thể chứa khoảng trắng
        
        # Kiểm tra key không chứa khoảng trắng
        if ' ' in key:
            return "400 BAD_REQUEST"
        
        is_new = key not in self.store
        self.store[key] = value
        
        return "201 CREATED" if is_new else "200 OK"
    
    def handle_get(self, args):
        """Xử lý lệnh GET key"""
        if len(args) != 1:
            return "400 BAD_REQUEST"
        
        key = args[0]
        if key in self.store:
            return f"200 OK {self.store[key]}"
        else:
            return "404 NOT_FOUND"
    
    def handle_del(self, args):
        """Xử lý lệnh DEL key"""
        if len(args) != 1:
            return "400 BAD_REQUEST"
        
        key = args[0]
        if key in self.store:
            del self.store[key]
            return "204 NO_CONTENT"
        else:
            return "404 NOT_FOUND"
    
    def handle_stats(self):
        """Xử lý lệnh STATS"""
        uptime = int(time.time() - self.stats['start_time'])
        keys_count = len(self.store)
        served = self.stats['served_requests']
        
        return f"200 OK keys={keys_count} uptime={uptime}s served={served}"
    
    def handle_quit(self):
        """Xử lý lệnh QUIT"""
        return "200 OK bye"

if __name__ == "__main__":
    server = KVSSServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nĐang tắt server...")
        server.logger.info("Server đã được tắt")
