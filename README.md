# 📘 SMS – Kubernetes GitOps Production Project

A **production-ready School Management System (SMS)** deployed on Kubernetes using **GitOps with ArgoCD**.
This project demonstrates real-world DevOps practices: containerization, stateful workloads, health checks, and automated deployments.

---

## 🚀 Live URLs

* **Frontend:** [http://sohaildevops.site](http://sohaildevops.site)
* **Backend API:** [http://sohaildevops.site/api](http://sohaildevops.site/api)
* **Health Check:** [http://sohaildevops.site/healthz/](http://sohaildevops.site/healthz/)
* **ArgoCD UI:** http://<NODE-IP>:8080

---

## 🧱 Architecture

```
Users
  │
  ▼
NGINX Ingress Controller
  │
  ├── React Frontend (Deployment + ClusterIP)
  │
  └── Django Backend (Deployment + ClusterIP)
        │
        └── PostgreSQL (StatefulSet + PVC)
```

---

## ⚙️ Technology Stack

* **Kubernetes** (kubeadm)
* **Docker**
* **ArgoCD** (GitOps)
* **Django + Gunicorn** (Backend)
* **React** (Frontend)
* **PostgreSQL** (StatefulSet)
* **NGINX Ingress Controller**
* **Calico CNI**
* **Metrics Server**
* **HPA & PDB**
* **Dynamic PVC via StorageClass**

---

## 📂 Repository Structure

```
sms-gitops/
├── namespace.yaml
├── backend/
│   ├── deployment.yaml
│   └── service.yaml
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
├── database/
│   ├── postgres-statefulset.yaml
│   └── service.yaml
├── ingress/
│   └── sms-ingress.yaml
```

---

## 🔄 GitOps Workflow (ArgoCD)

1. Developer pushes code or manifests to GitHub
2. ArgoCD detects changes automatically
3. Kubernetes cluster syncs to Git state
4. Self-healing and auto-rollback enabled

✔ No manual `kubectl apply`
✔ Git is the single source of truth

---

## 🗄️ Database (Production Setup)

* PostgreSQL deployed as **StatefulSet**
* **Dynamic PVC provisioning** using StorageClass
* No manual PV/PVC creation
* Persistent data survives pod restarts

---

## ❤️ Health Checks (Production)

* Django exposes `/healthz/`
* Kubernetes **liveness & readiness probes** enabled
* Supports **zero-downtime rolling updates**

---

## 🧪 Migrations (Production Safe)

* Django migrations executed via **InitContainer**
* App starts only after migrations succeed
* Fully automated & GitOps-friendly

---

## 🔐 Security Notes (Next Improvements)

* Database credentials should be moved to **Kubernetes Secrets**
* TLS (HTTPS) can be enabled via **cert-manager**
* ArgoCD admin access should be restricted

---

## 👨‍💻 Author

**Mohammed Sohail**
DevOps Engineer

* GitHub: [https://github.com/sohail-24](https://github.com/sohail-24)
* Docker Hub: [https://hub.docker.com/u/sohail28](https://hub.docker.com/u/sohail28)

---

## 🏁 Project Status

✅ Production-ready
✅ GitOps enabled
✅ Stateful database
✅ Health checks & migrations
✅ Interview-ready DevOps project
