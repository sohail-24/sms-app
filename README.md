# School Management System (SMS) – Kubernetes Deployment 🚀

This repository contains **Kubernetes manifests** for deploying a **School Management System (SMS)** application on an AWS EC2–based Kubernetes cluster.

The application image is **already built and pushed to Docker Hub**, and Kubernetes directly pulls and runs the image.

---

## 🔧 Tech Stack

* **Backend:** Django
* **Database:** PostgreSQL
* **Containerization:** Docker
* **Orchestration:** Kubernetes
* **Cloud:** AWS EC2 (Ubuntu)
* **Container Registry:** Docker Hub

---

## 📦 Docker Image

Pre-built Docker image used by Kubernetes:

```
sohail28/sms:latest
```

No image build is performed inside Kubernetes.

---

## 📁 Repository Structure

```
.
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── README.md
```

This repository is intentionally focused on **Kubernetes deployment only**.

---

## 🚀 Deployment Steps

### 1️⃣ Prerequisites

* Kubernetes cluster running
* `kubectl` configured
* Internet access to pull Docker images

---

### 2️⃣ Deploy to Kubernetes

```bash
kubectl apply -f k8s/
```

Verify:

```bash
kubectl get pods
kubectl get svc
```

---

## 🌐 Accessing the Application

### Port Forward (Development / Demo)

```bash
kubectl port-forward svc/sms-service 9090:80 --address 0.0.0.0
```

Browser:

```
http://<EC2-PUBLIC-IP>:9090/dashboard/
```

Available modules:

* Dashboard
* Students
* Teachers
* Courses
* Calendar
* Timetable
* Reports
* Examinations

---

## 📊 Features

* Student & Teacher Management
* Course Management
* Attendance Tracking
* Calendar & Timetable
* Exams & Reports
* Admin Dashboard

---

## 🧠 DevOps Design Decisions

* Docker used only for image creation
* Kubernetes handles runtime orchestration
* No docker-compose (not used in Kubernetes)
* Simple and clean deployment flow

---

## 👨‍💻 Author

**Mohammed Sohail**
DevOps Engineer (Fresher / 0–2 Years)

---

## 📌 Notes

* Ideal for learning and demos
* CI/CD can be added later if required
