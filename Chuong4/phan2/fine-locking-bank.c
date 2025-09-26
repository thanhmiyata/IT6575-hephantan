#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>

#define INIT_BALANCE 50
#define NUM_TRANS 50000

int balance = INIT_BALANCE;
int credits = 0;
int debits = 0;

// Fine locking: 3 mutex riêng biệt
pthread_mutex_t b_lock, c_lock, d_lock;

void * transactions(void * args){
    int i, v;
    for(i = 0; i < NUM_TRANS; i++){
        // choose a random value
        srand(time(NULL));
        v = rand() % NUM_TRANS;
        
        // randomly choose to credit or debit
        if(rand() % 2){
            // credit
            pthread_mutex_lock(&b_lock);
            balance = balance + v;
            pthread_mutex_unlock(&b_lock);
            
            pthread_mutex_lock(&c_lock);
            credits = credits + v;
            pthread_mutex_unlock(&c_lock);
        } else {
            // debit
            pthread_mutex_lock(&b_lock);
            balance = balance - v;
            pthread_mutex_unlock(&b_lock);
            
            pthread_mutex_lock(&d_lock);
            debits = debits + v;
            pthread_mutex_unlock(&d_lock);
        }
    }
    return 0;
}

int main(int argc, char * argv[]){
    int n_threads, i;
    pthread_t * threads;
    struct timespec start, end;
    double time_taken;
    
    printf("=== CÂU HỎI 8: FINE LOCKING BANKING ===\n");
    
    // error check
    if(argc < 2){
        fprintf(stderr, "ERROR: Require number of threads\n");
        exit(1);
    }
    
    // convert string to int
    n_threads = atol(argv[1]);
    
    // error check
    if(n_threads <= 0){
        fprintf(stderr, "ERROR: Invalid value for number of threads\n");
        exit(1);
    }
    
    printf("Số luồng: %d\n", n_threads);
    printf("Số giao dịch mỗi luồng: %d\n", NUM_TRANS);
    printf("Balance ban đầu: %d\n", INIT_BALANCE);
    
    // Khởi tạo 3 mutex
    pthread_mutex_init(&b_lock, NULL);
    pthread_mutex_init(&c_lock, NULL);
    pthread_mutex_init(&d_lock, NULL);
    
    // allocate array of thread identifiers
    threads = calloc(n_threads, sizeof(pthread_t));
    
    // Đo thời gian bắt đầu
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // start all threads
    for(i = 0; i < n_threads; i++){
        pthread_create(&threads[i], NULL, transactions, NULL);
    }
    
    // wait for all threads finish its jobs
    for(i = 0; i < n_threads; i++){
        pthread_join(threads[i], NULL);
    }
    
    // Đo thời gian kết thúc
    clock_gettime(CLOCK_MONOTONIC, &end);
    time_taken = (end.tv_sec - start.tv_sec) * 1e9;
    time_taken = (time_taken + (end.tv_nsec - start.tv_nsec)) * 1e-9;
    
    printf("\n=== KẾT QUẢ ===\n");
    printf("\tCredits:\t%d\n", credits);
    printf("\tDebits:\t\t%d\n\n", debits);
    printf("Tính toán lý thuyết: %d + %d - %d = %d\n", 
           INIT_BALANCE, credits, debits, INIT_BALANCE + credits - debits);
    printf("Balance thực tế:\t%d\n", balance);
    
    int difference = balance - (INIT_BALANCE + credits - debits);
    printf("Chênh lệch:\t\t%d\n", difference);
    printf("Thời gian thực hiện:\t%.6f giây\n", time_taken);
    
    if(difference != 0){
        printf("✗ Vẫn có vấn đề!\n");
    } else {
        printf("✓ Fine locking hoạt động tốt!\n");
    }
    
    // Hủy 3 mutex
    pthread_mutex_destroy(&b_lock);
    pthread_mutex_destroy(&c_lock);
    pthread_mutex_destroy(&d_lock);
    
    // free array
    free(threads);
    return 0;
}