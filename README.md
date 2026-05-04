🎓 UniEvent — University Event Management System

![AWS](https://img.shields.io/badge/AWS-Deployed-orange)
![Python](https://img.shields.io/badge/Python-Flask-blue)
![Status](https://img.shields.io/badge/Status-Live-green)

A scalable, fault-tolerant university event management web application hosted on AWS, fetching real events from the Ticketmaster API.

---

## 🏗️ Architecture Overview

The application uses the following AWS services:

- **VPC** — Isolated network with 4 subnets across 2 Availability Zones
- **EC2** — Two t3.micro instances running Flask in private subnets
- **ALB** — Application Load Balancer distributing traffic across both instances
- **S3** — Stores event data (JSON) and event images
- **IAM** — Role-based access control for EC2 to access S3 and CloudWatch
- **NAT Gateway** — Allows private EC2 instances to reach the Ticketmaster API
- **Security Groups** — Firewall rules restricting access between components

---

## 🔐 Security Design

- EC2 instances have **no public IP addresses**
- Instances live in **private subnets** — unreachable from the internet directly
- Only the **Load Balancer** can send traffic to EC2 instances
- S3 bucket has **all public access blocked**
- API keys stored in `.env` file — **never committed to GitHub**
- IAM role follows **least privilege** principle

---

## ⚡ Fault Tolerance

The system uses **2 EC2 instances across 2 Availability Zones**. If one instance or AZ goes down, the Load Balancer automatically routes all traffic to the healthy instance. This was tested by stopping Instance 1 — the website continued serving traffic through Instance 2 without any interruption.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python / Flask |
| Cloud Provider | AWS |
| Event Data | Ticketmaster Discovery API |
| Storage | Amazon S3 |
| Load Balancing | AWS Application Load Balancer |
| Compute | Amazon EC2 (Amazon Linux 2023) |
| Networking | AWS VPC, Subnets, NAT Gateway |

---

## 📁 Repository Structure
unievents-aws/
├── infrastructure/
│     └── vpc.md
├── application/
│     ├── app.py
│     └── .env.example
├── screenshots/
└── README.md

---

## 🚀 How to Run Locally

1. Clone the repo:
```bash
git clone https://github.com/yourusername/unievents-aws.git
```

2. Install dependencies:
```bash
pip3 install flask boto3 requests python-dotenv
```

3. Create `.env` file:
TICKETMASTER_API_KEY=your_api_key_here
S3_BUCKET_NAME=your_bucket_name_here

4. Run the app:
```bash
python3 app.py
```

---

## 📸 Screenshots

### Live Website
![Website](screenshots/Screenshot%202026-05-04%20135010.png)

### EC2 Instances
![EC2](screenshots/Screenshot%202026-05-04%20135030.png)

### Load Balancer
![ALB](screenshots/Screenshot%202026-05-04%20135228.png)

### S3 Bucket
![S3](screenshots/Screenshot%202026-05-04%20135529.png)

### VPC
![VPC](screenshots/Screenshot%202026-05-04%20135413.png)

---

## 📝 Notes

- HTTPS can be added using **AWS Certificate Manager (ACM)** with an SSL certificate attached to the Load Balancer
- The NAT Gateway and ALB incur charges even when EC2 instances are stopped
- SSM Session Manager was used for EC2 access instead of SSH/PuTTY

---

## 👨‍💻 Author

**Abdul Wadood**  
University Cloud Computing Assignment — AWS Infrastructure Project
