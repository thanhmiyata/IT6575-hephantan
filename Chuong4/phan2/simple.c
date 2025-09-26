#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <time.h>

int shared = 10;

void * fun(void * args){
    time_t start = time(NULL);
    time_t end = start + 5; // chạy trong 5 giây

    while (time(NULL) < end) {
    }
    shared++;

    return NULL;
}

int main(){
    pthread_t thread_id;
    
    printf("=== CÂU HỎI 4: SIMPLE THREADING ===\n");
    printf("Giá trị ban đầu của shared: %d\n", shared);
    
    pthread_create(&thread_id, NULL, fun, NULL);
    pthread_join(thread_id, NULL);
    
    printf("Giá trị cuối cùng của shared: %d\n", shared);
    printf("Số lần tăng trong 5 giây: %d\n", shared - 10);
    
    return 0;
}