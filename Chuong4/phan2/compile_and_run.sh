#!/bin/bash

echo "======================================"
echo "      BIÊN DỊCH VÀ CHẠY CHƯƠNG TRÌNH C"
echo "======================================"

# Biên dịch tất cả file C
echo "Bước 1: Biên dịch các file C..."

gcc -pthread simple.c -o simple
gcc -pthread without-lock.c -o without-lock
gcc -pthread naive-lock.c -o naive-lock
gcc -pthread mutex-lock-banking.c -o mutex-lock-banking
gcc -pthread fine-locking-bank.c -o fine-locking-bank
gcc -pthread deadlocks-test.c -o deadlocks-test

if [ $? -eq 0 ]; then
    echo "✓ Biên dịch thành công!"
    echo ""
    
    echo "======================================"
    echo "         CÁC LỆNH CHẠY"
    echo "======================================"
    echo "Câu hỏi 4: ./simple"
    echo "Câu hỏi 5: ./without-lock 5"
    echo "Câu hỏi 6: ./naive-lock 3"
    echo "Câu hỏi 7: ./mutex-lock-banking 5"
    echo "Câu hỏi 8: ./fine-locking-bank 5"
    echo "Câu hỏi 9: ./deadlocks-test"
    echo ""
    echo "VÍ DỤ CHẠY CÂU HỎI 5:"
    echo "----------------------"
    ./without-lock 5
    
else
    echo "✗ Lỗi biên dịch!"
fi