#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>

int lock = 0; // 0 for unlocked, 1 for locked
int shared = 0; // shared variable

void * incrementer(void * args){
    int i;
    for(i = 0; i < 100; i++){
        // check lock
        while(lock > 0);     // ← VẤN ĐỀ 1: Spin wait
        lock = 1;            // ← VẤN ĐỀ 2: Set lock  
        shared++;            // ← Critical section
        lock = 0;            // ← VẤN ĐỀ 3: Unlock
    }
    return NULL;
}

int main(int argc, char * argv[]){
    pthread_t * threads;
    int n, i;
    
    printf("=== CÂU HỏI 6: NAIVE LOCK ===\n");
    
    if(argc < 2){
        fprintf(stderr, "ERROR: Invalid number of threads\n");
        exit(1);
    }
    
    // convert argv[1] to a long
    if((n = atol(argv[1])) == 0){
        fprintf(stderr, "ERROR: Invalid number of threads\n");
        exit(1);
    }
    
    printf("Số luồng: %d\n", n);
    printf("Mỗi luồng tăng shared 100 lần\n");
    
    // allocate array of pthread_t identifiers
    threads = calloc(n, sizeof(pthread_t));
    
    // create n threads
    for(i = 0; i < n; i++){
        pthread_create(&threads[i], NULL, incrementer, NULL);
    }
    
    // join all threads
    for(i = 0; i < n; i++){
        pthread_join(threads[i], NULL);
    }
    
    // print shared value and result
    printf("\n=== KẾT QUẢ ===\n");
    printf("Shared thực tế: %d\n", shared);
    printf("Shared mong đợi: %d\n", n * 100);
    
    if(shared == n * 100){
        printf("✓ Kết quả chính xác!\n");
    } else {
        printf("✗ Naive lock có vấn đề! Chênh lệch: %d\n", (n * 100) - shared);
    }
    
    free(threads);
    return 0;
}