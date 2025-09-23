# 🗄️ Mini Key-Value Store Service (KVSS)
**Bài thực hành Interface trong Hệ thống Phân tán - IT6575**

## 📁 Cấu trúc project

```
BTL/
├── 📁 Chuong1/                   # Chương 1: Key-Value Store Service (KVSS)
│   ├── 📄 kvss_server.py         # KVSS Server implementation (TCP multi-threaded)
│   ├── 📄 kvss_client.py         # KVSS Client (interactive & batch modes)
│   ├── 🧪 test_kvss.py           # Automated test suite (10 test cases)
│   ├── 📊 kvss_server.log        # Server runtime logs (auto-generated)
│   └── 🐍 venv/                  # Python virtual environment
│
├── 📁 Chuong2/                   # Chương 2: Kubernetes Microservices Lab
│   └── 📁 k8s-microservices-lab/ # Kubernetes deployment configurations
│       ├── catalog-deploy.yaml   # Catalog service deployment
│       ├── gateway-ingress.yaml  # Ingress gateway configuration
│       ├── namespace.yaml        # Kubernetes namespace definition
│       ├── orders-deploy.yaml    # Orders service deployment
│       └── users-deploy.yaml     # Users service deployment
│
├── 📚 README.md                  # Project documentation (this file)
├── 📖 btlt_chap1_tongquan_kientruc_vie.pdf  # Course materials
└── 📖 btth_ch1_tongquan_kientruc_vie.pdf   # Lab instructions
```
