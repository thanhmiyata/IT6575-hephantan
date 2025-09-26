#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>

#define INIT_BALANCE 50
#define NUM_TRANS 100

int balance = INIT_BALANCE;
int credits = 0;
int debits = 0;

void * transactions(void * args){
    int i, v;
    for(i = 0; i < NUM_TRANS; i++){
        // choose a random value
        srand(time(NULL));
        v = rand() % NUM_TRANS;
        
        // randomly choose to credit or debit
        if(rand() % 2){
            // credit
            balance = balance + v;
            credits = credits + v;
        } else {
            // debit
            balance = balance - v;
            debits = debits + v;
        }
    }
    return 0;
}

int main(int argc, char * argv[]){
    int n_threads, i;
    pthread_t * threads;
    
    printf("=== CÂU HỎI 5: BANKING WITHOUT LOCK ===\n");
    
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
    
    // allocate array of thread identifiers
    threads = calloc(n_threads, sizeof(pthread_t));
    
    // start all threads
    for(i = 0; i < n_threads; i++){
        pthread_create(&threads[i], NULL, transactions, NULL);
    }
    
    // wait for all threads finish its jobs
    for(i = 0; i < n_threads; i++){
        pthread_join(threads[i], NULL);
    }
    
    printf("\n=== KẾT QUẢ ===\n");
    printf("\tCredits:\t%d\n", credits);
    printf("\tDebits:\t\t%d\n\n", debits);
    printf("Tính toán lý thuyết: %d + %d - %d = %d\n", 
           INIT_BALANCE, credits, debits, INIT_BALANCE + credits - debits);
    printf("Balance thực tế:\t%d\n", balance);
    
    int difference = balance - (INIT_BALANCE + credits - debits);
    printf("Chênh lệch:\t\t%d\n", difference);
    
    if(difference != 0){
        printf("✗ CÓ RACE CONDITION!\n");
    } else {
        printf("✓ Không có race condition\n");
    }
    
    // free array
    free(threads);
    return 0;
}