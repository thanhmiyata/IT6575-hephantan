public class Main {
    public static void main(String[] args) throws InterruptedException {
        // CÂU 1: Tạo thực thể resource với giá trị khởi tạo là 0
        // ResourcesExploiter resource = new ResourcesExploiter(0);

        // // Câu 1: Tạo 3 thực thể worker (SỬ DỤNG KHÔNG CÓ SYNCHRONIZED)
        // ThreadedWorkerWithoutSync worker1 = new ThreadedWorkerWithoutSync(resource);
        // ThreadedWorkerWithoutSync worker2 = new ThreadedWorkerWithoutSync(resource);
        // ThreadedWorkerWithoutSync worker3 = new ThreadedWorkerWithoutSync(resource);

        // Câu 2: Tạo 3 thực thể worker (SỬ DỤNG SYNCHRONIZED)
        // ThreadedWorkerWithSync worker1 = new ThreadedWorkerWithSync(resource);
        // ThreadedWorkerWithSync worker2 = new ThreadedWorkerWithSync(resource);
        // ThreadedWorkerWithSync worker3 = new ThreadedWorkerWithSync(resource);

        // CÂU 3: Tạo thực thể resource với ReentrantLock và worker với Lock
        ResourcesExploiterWithLock resource = new ResourcesExploiterWithLock(0);
        ThreadedWorkerWithLock worker1 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker2 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker3 = new ThreadedWorkerWithLock(resource);

        // Khởi động 3 luồng
        worker1.start();
        worker2.start();
        worker3.start();
        
        // Chờ các luồng kết thúc
        worker1.join();
        worker2.join();
        worker3.join();
        
        // In kết quả
        System.out.println("Giá trị thực tế của rsc: " + resource.getRsc());
    }
}