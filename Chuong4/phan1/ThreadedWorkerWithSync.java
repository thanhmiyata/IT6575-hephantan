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