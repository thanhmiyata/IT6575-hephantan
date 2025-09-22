# Hướng dẫn thực hành: Kiến trúc Microservices với Kubernetes trên macOS 15.6

## Tổng quan

Hướng dẫn này sẽ giúp bạn xây dựng một ứng dụng thương mại điện tử với 3 microservices (users, catalog, orders) sử dụng Kubernetes trên macOS 15.6 Sequoia. Chúng ta sẽ triển khai các Deployment, Service, và cấu hình Ingress làm API Gateway.

**Ngày cập nhật:** 22/09/2025  
**Môi trường:** macOS 15.6 (Sequoia)  
**Thời gian thực hiện:** 60-90 phút

## Mục tiêu học tập

- Hiểu kiến trúc Microservices và cách triển khai trên Kubernetes
- Thực hành với Pods, Services, Deployments
- Cấu hình Ingress Controller làm API Gateway
- Scale microservices và quan sát kết quả
- Xử lý các vấn đề thường gặp

## Phần 1: Cài đặt môi trường

### 1.1 Cài đặt Docker Desktop

```bash
# Tải Docker Desktop từ trang chính thức
# https://docs.docker.com/desktop/install/mac-install/

# Hoặc sử dụng Homebrew
brew install --cask docker

# Khởi động Docker Desktop và đảm bảo nó chạy
docker --version
```

### 1.2 Cài đặt kubectl

```bash
# Cách 1: Sử dụng Homebrew (khuyến nghị)
brew install kubectl

# Cách 2: Tải binary trực tiếp (nếu Homebrew lỗi)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Kiểm tra cài đặt
kubectl version --client
```

### 1.3 Cài đặt Minikube

```bash
# Cách 1: Sử dụng Homebrew
brew install minikube

# Cách 2: Tải binary trực tiếp
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube

# Kiểm tra cài đặt
minikube version
```

### 1.4 Khởi động Minikube

```bash
# Khởi động Minikube với Docker driver
minikube start --driver=docker

# Kiểm tra trạng thái nodes
kubectl get nodes

# Bật addon ingress
minikube addons enable ingress

# Kiểm tra ingress controller
kubectl get pods -n ingress-nginx
```

## Phần 2: Chuẩn bị file cấu hình YAML

### 2.1 Tạo cấu trúc thư mục

```bash
# Tạo thư mục dự án
mkdir -p ~/k8s-microservices-lab
cd ~/k8s-microservices-lab

# Tạo namespace file
cat > namespace.yaml << EOF
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
EOF
```

### 2.2 Tạo file users-deploy.yaml

```bash
cat > users-deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: users-deploy
  namespace: microservices
spec:
  replicas: 1
  selector:
    matchLabels:
      app: users
  template:
    metadata:
      labels:
        app: users
    spec:
      containers:
      - name: users
        image: nginx:alpine
        ports:
        - containerPort: 80
        env:
        - name: SERVICE_NAME
          value: "users"
        volumeMounts:
        - name: html-config
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html-config
        configMap:
          name: users-html
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: users-html
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Users Service</title></head>
    <body>
      <h1>Users Microservice</h1>
      <p>Service: users</p>
      <p>Hostname: <script>document.write(location.hostname)</script></p>
      <p>Timestamp: <script>document.write(new Date().toISOString())</script></p>
    </body>
    </html>
---
apiVersion: v1
kind: Service
metadata:
  name: users-service
  namespace: microservices
spec:
  selector:
    app: users
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
EOF
```

### 2.3 Tạo file catalog-deploy.yaml

```bash
cat > catalog-deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: catalog-deploy
  namespace: microservices
spec:
  replicas: 1
  selector:
    matchLabels:
      app: catalog
  template:
    metadata:
      labels:
        app: catalog
    spec:
      containers:
      - name: catalog
        image: nginx:alpine
        ports:
        - containerPort: 80
        env:
        - name: SERVICE_NAME
          value: "catalog"
        volumeMounts:
        - name: html-config
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html-config
        configMap:
          name: catalog-html
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: catalog-html
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Catalog Service</title></head>
    <body>
      <h1>Catalog Microservice</h1>
      <p>Service: catalog</p>
      <p>Hostname: <script>document.write(location.hostname)</script></p>
      <p>Timestamp: <script>document.write(new Date().toISOString())</script></p>
      <div id="products">
        <h2>Products:</h2>
        <ul>
          <li>Product 1 - $10</li>
          <li>Product 2 - $20</li>
          <li>Product 3 - $30</li>
        </ul>
      </div>
    </body>
    </html>
---
apiVersion: v1
kind: Service
metadata:
  name: catalog-service
  namespace: microservices
spec:
  selector:
    app: catalog
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
EOF
```

### 2.4 Tạo file orders-deploy.yaml

```bash
cat > orders-deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-deploy
  namespace: microservices
spec:
  replicas: 1
  selector:
    matchLabels:
      app: orders
  template:
    metadata:
      labels:
        app: orders
    spec:
      containers:
      - name: orders
        image: nginx:alpine
        ports:
        - containerPort: 80
        env:
        - name: SERVICE_NAME
          value: "orders"
        volumeMounts:
        - name: html-config
          mountPath: /usr/share/nginx/html
      volumes:
      - name: html-config
        configMap:
          name: orders-html
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: orders-html
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Orders Service</title></head>
    <body>
      <h1>Orders Microservice</h1>
      <p>Service: orders</p>
      <p>Hostname: <script>document.write(location.hostname)</script></p>
      <p>Timestamp: <script>document.write(new Date().toISOString())</script></p>
      <div id="orders">
        <h2>Recent Orders:</h2>
        <ul>
          <li>Order #001 - $50 - Pending</li>
          <li>Order #002 - $75 - Completed</li>
          <li>Order #003 - $120 - Processing</li>
        </ul>
      </div>
    </body>
    </html>
---
apiVersion: v1
kind: Service
metadata:
  name: orders-service
  namespace: microservices
spec:
  selector:
    app: orders
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
EOF
```

### 2.5 Tạo file gateway-ingress.yaml

```bash
cat > gateway-ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservices-ingress
  namespace: microservices
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: micro.local
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: users-service
            port:
              number: 80
      - path: /catalog
        pathType: Prefix
        backend:
          service:
            name: catalog-service
            port:
              number: 80
      - path: /orders
        pathType: Prefix
        backend:
          service:
            name: orders-service
            port:
              number: 80
EOF
```

## Phần 3: Triển khai ứng dụng

### 3.1 Tạo namespace và triển khai services

```bash
# Tạo namespace
kubectl apply -f namespace.yaml

# Triển khai users service
kubectl apply -f users-deploy.yaml

# Triển khai catalog service
kubectl apply -f catalog-deploy.yaml

# Triển khai orders service
kubectl apply -f orders-deploy.yaml

# Triển khai ingress
kubectl apply -f gateway-ingress.yaml
```

### 3.2 Kiểm tra triển khai

**Câu 6: Sau khi chạy `kubectl apply -f users-deploy.yaml`, dùng lệnh nào để kiểm tra Pod của service users đã chạy thành công?**

```bash
# Kiểm tra pods trong namespace microservices
kubectl get pods -n microservices

# Kiểm tra chi tiết pod users
kubectl get pods -n microservices -l app=users

# Kiểm tra trạng thái chi tiết
kubectl describe pod -n microservices -l app=users
```

**Hướng dẫn chụp màn hình:** Chụp màn hình kết quả lệnh `kubectl get pods -n microservices` để thấy trạng thái "Running" của pod users.

```bash
# Kiểm tra tất cả services
kubectl get svc -n microservices

# Kiểm tra ingress
kubectl get ingress -n microservices
```

## Phần 4: Cấu hình truy cập

### 4.1 Khởi động Minikube tunnel

```bash
# Mở terminal mới và chạy lệnh này (giữ terminal này mở)
minikube tunnel
```

### 4.2 Cấu hình /etc/hosts

**Câu 8: Sau khi cài Ingress, em cần thêm dòng nào vào file /etc/hosts để truy cập bằng tên miền micro.local?**

```bash
# Lấy IP của Minikube
minikube ip

# Hoặc lấy IP từ ingress
kubectl get ingress -n microservices

# Thêm vào /etc/hosts (thay <MINIKUBE_IP> bằng IP thực tế)
echo "127.0.0.1 micro.local" | sudo tee -a /etc/hosts

# Kiểm tra file hosts
cat /etc/hosts | grep micro.local
```

**Trả lời Câu 8:** Cần thêm dòng `127.0.0.1 micro.local` vào file `/etc/hosts`

## Phần 5: Kiểm tra ứng dụng

### 5.1 Kiểm tra qua trình duyệt

```bash
# Mở các URL sau trong trình duyệt:
# http://micro.local/users
# http://micro.local/catalog  
# http://micro.local/orders
```

### 5.2 Kiểm tra bằng curl

```bash
# Kiểm tra users service
curl -H "Host: micro.local" http://127.0.0.1/users

# Kiểm tra catalog service
curl -H "Host: micro.local" http://127.0.0.1/catalog

# Kiểm tra orders service
curl -H "Host: micro.local" http://127.0.0.1/orders
```

**Hướng dẫn chụp màn hình:** Chụp màn hình kết quả curl hoặc trình duyệt cho cả 3 services.

## Phần 6: Scale microservice

### 6.1 Scale catalog service

```bash
# Scale catalog từ 1 replica lên 3 replicas
kubectl scale deployment catalog-deploy --replicas=3 -n microservices

# Kiểm tra kết quả
kubectl get pods -n microservices -l app=catalog

# Xem chi tiết deployment
kubectl get deployment catalog-deploy -n microservices
```

**Hướng dẫn chụp màn hình:** Chụp màn hình kết quả `kubectl get pods -n microservices` để thấy 3 pods catalog đang chạy.

### 6.2 Kiểm tra load balancing

```bash
# Gọi API nhiều lần để thấy load balancing
for i in {1..10}; do
  curl -s -H "Host: micro.local" http://127.0.0.1/catalog | grep -i hostname
  sleep 1
done
```

## Phần 7: Phân tích cấu hình (Trả lời Câu 7)

**Câu 7: Trong file users-deploy.yaml, hãy chỉ ra:**
- **Deployment quản lý bao nhiêu replica ban đầu?**
- **Service thuộc loại nào (ClusterIP, NodePort, LoadBalancer)?**

```bash
# Kiểm tra số replica trong deployment
kubectl get deployment users-deploy -n microservices -o yaml | grep replicas

# Kiểm tra loại service
kubectl get service users-service -n microservices -o yaml | grep type
```

**Trả lời Câu 7:**
- Deployment quản lý **1 replica** ban đầu (dòng `replicas: 1`)
- Service thuộc loại **ClusterIP** (dòng `type: ClusterIP`)

## Phần 8: Xử lý sự cố thường gặp

### 8.1 Pod không start được

```bash
# Xem logs của pod
kubectl logs -n microservices -l app=users

# Xem events
kubectl get events -n microservices --sort-by=.metadata.creationTimestamp

# Describe pod để xem chi tiết lỗi
kubectl describe pod -n microservices -l app=users
```

### 8.2 Ingress không hoạt động

```bash
# Kiểm tra ingress controller
kubectl get pods -n ingress-nginx

# Kiểm tra ingress
kubectl describe ingress microservices-ingress -n microservices

# Restart ingress controller nếu cần
kubectl delete pod -n ingress-nginx -l app.kubernetes.io/component=controller
```

### 8.3 Không truy cập được qua domain

```bash
# Kiểm tra minikube tunnel đang chạy
ps aux | grep "minikube tunnel"

# Kiểm tra /etc/hosts
cat /etc/hosts | grep micro.local

# Test DNS resolution
nslookup micro.local
```

## Phần 9: Dọn dẹp

### 9.1 Xóa resources

```bash
# Xóa tất cả resources trong namespace
kubectl delete namespace microservices

# Hoặc xóa từng file
kubectl delete -f gateway-ingress.yaml
kubectl delete -f orders-deploy.yaml
kubectl delete -f catalog-deploy.yaml
kubectl delete -f users-deploy.yaml
kubectl delete -f namespace.yaml
```

### 9.2 Dọn dẹp hệ thống

```bash
# Dừng minikube
minikube stop

# Xóa cluster (nếu muốn)
minikube delete

# Xóa dòng trong /etc/hosts
sudo sed -i '' '/micro.local/d' /etc/hosts
```

### 9.3 Xóa files

```bash
# Xóa thư mục dự án
cd ~
rm -rf k8s-microservices-lab
```

## Kết luận

Bạn đã thành công:
- ✅ Triển khai 3 microservices trên Kubernetes
- ✅ Cấu hình Ingress làm API Gateway  
- ✅ Scale microservice từ 1 lên 3 replicas
- ✅ Kiểm tra load balancing
- ✅ Trả lời các câu hỏi lý thuyết

### Điểm cần nhớ:
- **Microservices** giúp chia nhỏ ứng dụng thành các service độc lập
- **Kubernetes** cung cấp orchestration cho containers
- **Ingress** hoạt động như reverse proxy/API gateway
- **Scaling** giúp tăng khả năng chịu tải của hệ thống

### Tài liệu tham khảo:
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

**Lưu ý:** Nhớ chụp màn hình các bước quan trọng để nộp báo cáo!
