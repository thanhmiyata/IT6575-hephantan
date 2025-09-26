# CHƯƠNG 4: ĐỒNG BỘ HÓA - BÀI THỰC HÀNH

## Tổng quan
Bài thực hành về đồng bộ hóa trong hệ phân tán, bao gồm:
- **Phần 1**: Triển khai đồng bộ luồng trong Java
- **Phần 2**: Lập trình song song với đoạn găng trong C

---

## PHẦN 1: ĐỒNG BỘ HÓA LUỒNG TRONG JAVA

### Bước 1: Tạo lớp ResourcesExploiter
**File**: `ResourcesExploiter.java`

```java
public class ResourcesExploiter {
    private int rsc;
    
    public ResourcesExploiter(int n) {
        rsc = n;
    }
    
    public void setRsc(int n) {
        rsc = n;
    }
    
    public int getRsc() {
        return rsc;
    }
    
    public void exploit() {
        setRsc(getRsc() + 1);
    }
}
```

### Bước 2: Tạo ThreadedWorkerWithoutSync
**File**: `ThreadedWorkerWithoutSync.java`

```java
public class ThreadedWorkerWithoutSync extends Thread {
    private ResourcesExploiter rExp;
    
    public ThreadedWorkerWithoutSync(ResourcesExploiter resource) {
        this.rExp = resource;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}
```

### Bước 3: Tạo lớp Main và test không đồng bộ
**File**: `MainWithoutSync.java`

```java
public class MainWithoutSync {
    public static void main(String[] args) throws InterruptedException {
        ResourcesExploiter resource = new ResourcesExploiter(0);
        
        ThreadedWorkerWithoutSync worker1 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker2 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker3 = new ThreadedWorkerWithoutSync(resource);
        
        worker1.start();
        worker2.start();
        worker3.start();
        
        worker1.join();
        worker2.join();
        worker3.join();
        
        System.out.println("Kết quả rsc: " + resource.getRsc());
        System.out.println("Kết quả mong đợi: 3000");
    }
}
```

**Câu hỏi 1**: Chạy chương trình nhiều lần. Bạn sẽ thấy kết quả không ổn định, thường < 3000 do **race condition** - nhiều luồng cùng truy cập và sửa đổi biến `rsc` mà không có đồng bộ.

### Bước 4: Tạo ThreadedWorkerWithSync
**File**: `ThreadedWorkerWithSync.java`

```java
public class ThreadedWorkerWithSync extends Thread {
    private ResourcesExploiter rExp;
    
    public ThreadedWorkerWithSync(ResourcesExploiter resource) {
        this.rExp = resource;
    }
    
    @Override
    public void run() {
        synchronized(rExp) {
            for (int i = 0; i < 1000; i++) {
                rExp.exploit();
            }
        }
    }
}
```

**Câu hỏi 2**: Thay thế worker trong main bằng `ThreadedWorkerWithSync`. Kết quả sẽ luôn là 3000 vì `synchronized` đảm bảo chỉ có 1 luồng được thực thi tại một thời điểm.

### Bước 5: Tạo ResourcesExploiterWithLock
**File**: `ResourcesExploiterWithLock.java`

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class ResourcesExploiterWithLock extends ResourcesExploiter {
    private ReentrantLock lock;
    
    public ResourcesExploiterWithLock(int n) {
        super(n);
        lock = new ReentrantLock();
    }
    
    @Override
    public void exploit() {
        try {
            if (lock.tryLock(10, TimeUnit.SECONDS)) {
                setRsc(getRsc() + 1);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}
```

### Bước 6: Tạo ThreadedWorkerWithLock
**File**: `ThreadedWorkerWithLock.java`

```java
public class ThreadedWorkerWithLock extends Thread {
    private ResourcesExploiterWithLock rExp;
    
    public ThreadedWorkerWithLock(ResourcesExploiterWithLock resource) {
        this.rExp = resource;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}
```

**Câu hỏi 3**: Sử dụng ReentrantLock cho kết quả tương tự synchronized nhưng linh hoạt hơn với timeout và các tính năng nâng cao.

---

## PHẦN 2: LẬP TRÌNH SONG SONG TRONG C

### Bước 7: Tạo simple.c
**File**: `simple.c`

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <time.h>

int shared = 10;

void * fun(void * args){
    time_t start = time(NULL);
    time_t end = start + 5; // run for 5 seconds
    
    // YOUR-CODE-HERE
    while (time(NULL) < end) {
        shared++;
    }
    
    return NULL;
}

int main(){
    pthread_t thread_id;
    pthread_create(&thread_id, NULL, fun, NULL);
    pthread_join(thread_id, NULL);
    printf("shared: %d\n", shared);
    return 0;
}
```

**Biên dịch và chạy**:
```bash
gcc -pthread simple.c -o simple
./simple
```

**Câu hỏi 4**: Chương trình tăng biến `shared` liên tục trong 5 giây bằng vòng lặp `while`.

### Bước 8: Tạo without-lock.c
**File**: `without-lock.c` (sử dụng code đã cho trong đề bài)

**Biên dịch và chạy**:
```bash
gcc -pthread without-lock.c -o without-lock
./without-lock 5
```

**Câu hỏi 5**: Khi tăng số luồng và `NUM_TRANS`, sẽ thấy sự khác biệt giữa Balance thực tế và `INIT_BALANCE+credits-debits` do **race condition** khi nhiều luồng cùng thao tác trên các biến chung.

### Bước 9: Tạo naive-lock.c
**File**: `naive-lock.c` (sử dụng code đã cho)

**Câu hỏi 6**: Naive lock có thể fail vì giữa thời điểm check `while(lock > 0)` và set `lock = 1` có thể có luồng khác chen vào.

### Bước 10: Tạo mutex-lock-banking.c
**File**: `mutex-lock-banking.c`

Sửa đổi `without-lock.c`:
```c
// Thêm mutex
pthread_mutex_t mutex;

// Trong main()
pthread_mutex_init(&mutex, NULL);

// Trong transactions()
pthread_mutex_lock(&mutex);
// Critical section code
pthread_mutex_unlock(&mutex);

// Cuối main()
pthread_mutex_destroy(&mutex);
```

**Câu hỏi 7**: Mutex lock atomic và reliable hơn naive lock, đảm bảo không có race condition.

### Bước 11: Tạo fine-locking-bank.c
**File**: `fine-locking-bank.c`

```c
pthread_mutex_t b_lock, c_lock, d_lock;

// Trong transactions()
pthread_mutex_lock(&b_lock);
balance = balance + v; // hoặc - v
pthread_mutex_unlock(&b_lock);

pthread_mutex_lock(&c_lock);
credits = credits + v;
pthread_mutex_unlock(&c_lock);

// Tương tự cho debits với d_lock
```

**Câu hỏi 8**: Fine locking nhanh hơn coarse locking vì các luồng có thể đồng thời thao tác trên các biến khác nhau.

### Bước 12: Tạo deadlocks-test.c
**File**: `deadlocks-test.c` (sử dụng code đã cho)

**Câu hỏi 9**: Chương trình sẽ bị **deadlock** vì:
- `fun_1` lock A trước, sau đó lock B
- `fun_2` lock B trước, sau đó lock A
- Khi cả hai cùng chạy, có thể xảy ra tình huống mỗi luồng giữ 1 lock và chờ lock kia → deadlock

---

## Cách biên dịch và chạy

### Java
```bash
javac *.java
java MainWithoutSync
java MainWithSync  # (sau khi sửa main)
```

### C
```bash
gcc -pthread filename.c -o filename
./filename [arguments]
```

---

## Kết luận
Bài thực hành giúp hiểu:
- **Race condition** và tầm quan trọng của đồng bộ hóa
- Các phương pháp đồng bộ: `synchronized`, `ReentrantLock`, `mutex`
- **Coarse vs Fine locking**
- **Deadlock** và cách tránh

## Tài liệu tham khảo
- Java Concurrency in Practice
- POSIX Threads Programming
- Operating System Concepts