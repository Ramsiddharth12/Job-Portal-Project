# Job Portal Backend API

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![JWT](https://img.shields.io/badge/Auth-JWT-success)
![Architecture](https://img.shields.io/badge/Architecture-Service%20Layer-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

# Live Architecture Overview

```text
                Internet Users
                        │
                        ▼
                Flask Backend API
                 (Docker Container)
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
   JWT Authentication            RBAC Authorization
         │                             │
         └──────────────┬──────────────┘
                        ▼
                Service Layer Logic
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
      Routes        Validators       Utilities
                        │
                        ▼
                 PostgreSQL Database
                  (Docker Container)
                        │
                        ▼
                Resume Upload Storage
```

---

# Overview

A production-style backend system simulating a real-world Job Portal platform, built using Flask and PostgreSQL with secure authentication, role-based authorization, resume uploads, and Dockerized infrastructure.

This project demonstrates:

* End-to-end backend engineering workflow
* JWT-based authentication system
* Role-Based Access Control (RBAC)
* Resume upload handling
* PostgreSQL database integration
* Dockerized multi-container setup
* Modular service architecture
* Scalable backend folder structure

The project was designed with real-world backend and DevOps practices in mind rather than simple CRUD-only implementation.

---

# What Makes This Project Strong

* Secure JWT-based authentication system
* Real-world RBAC implementation
* Dockerized Flask + PostgreSQL architecture
* Resume upload handling using form-data
* Service-layer backend structure
* Input validation architecture
* PostgreSQL migration from SQLite
* Recruiter/Admin permission management
* Modular scalable project structure
* Environment variable management using `.env`
* Separation of routes, services, validators, and utilities

---

# Features

## Authentication & Authorization

* Applicant Registration
* Recruiter Registration
* Admin Registration
* Secure Login System
* JWT Token Generation
* Protected Routes
* Role-Based Access Control

---

## Job Management

* Create Jobs
* Delete Jobs
* List Available Jobs
* Apply for Jobs
* List Applied Jobs

---

## Resume Upload System

* Resume upload using multipart/form-data
* Secure filename handling
* Local upload storage
* Upload directory auto-creation

---

## Dockerized Infrastructure

* Flask container
* PostgreSQL container
* Multi-container orchestration using Docker Compose
* Environment variable injection
* Persistent PostgreSQL volumes

---

# Tech Stack

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| Python 3.13        | Backend Programming         |
| Flask              | Backend Framework           |
| SQLAlchemy         | ORM                         |
| PostgreSQL         | Relational Database         |
| Flask-JWT-Extended | Authentication              |
| Docker             | Containerization            |
| Docker Compose     | Multi-container Management  |
| Werkzeug           | Password Hashing & Security |
| GitHub             | Version Control             |
| Postman            | API Testing                 |

---

# Project Structure

```text
Job-Portal-Project/
│
├── auth/
│   └── auth.py
│
├── routes/
│   └── BackendFlask.py
│
├── services/
│   └── operations.py
│
├── validators/
│   └── jobvalidator.py
│
├── utils/
│
├── uploads/
│
├── app.py
├── dbapp.py
├── models.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── .dockerignore
```

---

# Backend Architecture

## Route Layer

Handles:

* Request receiving
* JWT protection
* Role checks
* Calling services
* Returning responses

Example:

```python
@app.route("/listjobs")
def AllJobsList():
    jobs = Listjobs()
    return jsonify(jobs)
```

---

## Service Layer

Handles:

* Business logic
* Database operations
* Upload handling
* Main backend workflows

Example:

```python
new_application = Application(
    applicant_id=identity,
    job_id=job_id,
    resume_filename=filename
)
```

---

## Validator Layer

Handles:

* Input validation
* Required field checks
* Salary validation
* Job type validation

This improves:

* Code cleanliness
* Reusability
* Maintainability

---

## Utility Layer

Used for reusable helper functionality.

Future improvements planned:

* Response helpers
* Pagination utilities
* S3 upload helpers
* Logging helpers

---

# Role-Based Access Control (RBAC)

The application implements RBAC using JWT claims.

## Roles

| Role      | Permissions              |
| --------- | ------------------------ |
| Applicant | Apply for jobs           |
| Recruiter | Create/Delete jobs       |
| Admin     | Manage recruiters/admins |

---

## Authorization Example

```python
if Role != "admin":
    return jsonify({
        "success": False,
        "Error": "Access denied"
    }), 403
```

---

# End-to-End Workflow

# Applicant Workflow

```text
Register
   ↓
Login
   ↓
Receive JWT Token
   ↓
View Jobs
   ↓
Apply for Job
   ↓
Upload Resume
   ↓
Application Stored in PostgreSQL
```

---

# Recruiter Workflow

```text
Recruiter Login
        ↓
Create New Job
        ↓
Job Stored in PostgreSQL
        ↓
Applicants Apply
        ↓
Recruiter Reviews Applications
```

---

# Admin Workflow

```text
Admin Login
      ↓
Create Recruiters/Admins
      ↓
Manage System Access
      ↓
Control Platform Roles
```

---

# Docker Architecture

```text
                Postman / Client
                        │
                        ▼
               Flask API Container
                  (flask_app)
                        │
                        ▼
             PostgreSQL Container
                 (postgres_db)
                        │
                        ▼
              Persistent Docker Volume
```

---

# Docker Components

## Dockerfile

Responsible for:

* Building Flask image
* Installing dependencies
* Copying application files
* Running Flask app

---

## Docker Compose

Responsible for:

* Running multiple containers
* Connecting Flask and PostgreSQL
* Environment variable injection
* Persistent storage management
* Port mapping

---

## PostgreSQL Container

Configured using:

```yaml
image: postgres:17
```

Provides:

* Production-style relational database
* Persistent storage using Docker volumes
* Isolated database container

---

# Database Design

## User Table

Stores:

* User credentials
* Password hashes
* Roles
* Account creation timestamps

---

## Job Table

Stores:

* Job information
* Salary
* Skills
* Location
* Recruiter ownership

---

## Application Table

Stores:

* Applicant-job relationship
* Resume filename
* Application status
* Apply timestamps

---

# Database Relationships

```text
User
 ├── Jobs Created
 └── Applications

Job
 └── Applications

Application
 ├── Applicant
 └── Job
```

---

# Authentication Flow

```text
User Login
     ↓
Password Verification
     ↓
JWT Token Creation
     ↓
Client Stores Token
     ↓
Protected Route Access
     ↓
JWT Verification
```

---

# Resume Upload Flow

```text
Applicant Uploads Resume
            ↓
multipart/form-data Request
            ↓
Secure Filename Generation
            ↓
uploads/ Directory Creation
            ↓
Resume Saved Locally
            ↓
Filename Stored in PostgreSQL
```

---

# Design Decisions

# Why Flask?

Flask was chosen for its:

* Lightweight architecture
* Simplicity
* Flexibility
* Backend API friendliness
* Fast development workflow

---

# Why PostgreSQL?

PostgreSQL was selected because:

* Relational consistency
* Production readiness
* Better scalability
* Strong SQL support
* Widely used in industry systems

---

# Why Docker?

Docker was implemented to:

* Ensure environment consistency
* Simplify deployment
* Separate services cleanly
* Simulate production workflows
* Improve portability

---

# Why Service Layer Architecture?

Business logic was separated from routes to:

* Improve maintainability
* Reduce route complexity
* Support scalability
* Improve code organization
* Follow backend engineering practices

---

# Trade-Offs Considered

## Local Resume Storage Instead of AWS S3

Current implementation uses local uploads for simplicity during development.

Future versions may migrate to:

* AWS S3
* Cloud object storage
* CDN-based delivery

---

## Monolithic Architecture Instead of Microservices

A monolithic backend was chosen because:

* Faster development
* Easier debugging
* Lower infrastructure complexity
* Better beginner-to-intermediate scalability

Future migration to microservices may be explored.

---

## Manual Validators Instead of Pydantic/Marshmallow

Manual validators were initially implemented to:

* Understand validation fundamentals
* Improve backend logic understanding
* Reduce abstraction during learning phase

Future versions may integrate:

* Pydantic
* Marshmallow
* Schema-based validation

---

# Cost Optimization Considerations

This project considers infrastructure cost-awareness.

## Optimization Decisions

* Dockerized deployment reduces setup issues
* Single-server deployment initially
* PostgreSQL containerized locally
* Lightweight Flask backend
* Monolithic architecture for lower infra complexity

---

## Future Cost Optimization Ideas

* AWS S3 for scalable storage
* EC2 autoscaling
* NGINX reverse proxy caching
* CloudWatch monitoring
* Managed PostgreSQL services

---

# API Endpoints

## Authentication Routes

| Method | Endpoint           | Description            |
| ------ | ------------------ | ---------------------- |
| POST   | /register          | Applicant registration |
| POST   | /adminregister     | Admin registration     |
| POST   | /recruiterregister | Recruiter registration |
| POST   | /login             | User login             |

---

## Job Routes

| Method | Endpoint   | Description         |
| ------ | ---------- | ------------------- |
| POST   | /newjob    | Create new job      |
| GET    | /listjobs  | List available jobs |
| DELETE | /deletejob | Delete job          |

---

## Application Routes

| Method | Endpoint        | Description       |
| ------ | --------------- | ----------------- |
| POST   | /applyjob       | Apply for a job   |
| GET    | /listappliedjob | List applied jobs |

---

# Example API Request

## Apply for Job

### Request Type

```text
multipart/form-data
```

### Form Fields

| Key    | Type |
| ------ | ---- |
| job_id | Text |
| resume | File |

---

# Example Success Response

```json
{
    "success": true,
    "message": "successfully applied for the job"
}
```

---

# Environment Variables

Example `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/jobportal
JWT_SECRET_KEY=your_secret_key
```

---

# Docker Commands

## Build & Run Containers

```bash
docker compose up --build
```

---

## Stop Containers

```bash
docker compose down
```

---

## Enter Flask Container

```bash
docker exec -it flask_app bash
```

---

## Create Database Tables

```python
python

from app import app
from dbapp import db

app.app_context().push()

db.create_all()
```

---

# Screenshots

## Health Check

*Add screenshot here*

---

## Login Response

*Add screenshot here*

---

## List Jobs

*Add screenshot here*

---

## Apply Job with Resume Upload

*Add screenshot here*

---

## Docker Containers Running

*Add screenshot here*

---

# Future Improvements

## Backend Improvements

* Pagination support
* Centralized response utilities
* Better error handling
* Logging system
* Async task handling

---

## DevOps Improvements

* CI/CD pipeline
* GitHub Actions
* Docker Hub integration
* Terraform provisioning
* AWS deployment
* NGINX reverse proxy
* Kubernetes orchestration
* CloudWatch monitoring

---

## Cloud Improvements

* AWS S3 resume uploads
* EC2 deployment
* Load balancing
* Managed PostgreSQL
* Auto scaling

---

# Learning Outcomes

This project helped strengthen understanding of:

* Backend engineering
* Authentication systems
* RBAC implementation
* PostgreSQL integration
* Docker containerization
* Service architecture
* File upload handling
* API testing using Postman
* Environment management
* Real-world backend workflows

---

# Author

## Ram Siddharth

B.Tech Information Technology

Backend • DevOps • Cloud Learning Journey

---

