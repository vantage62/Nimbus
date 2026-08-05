# Deployment Guide

**Project:** Nimbus

**Version:** 1.0.0

**Status:** Production Deployment Design

---

# 1. Purpose

This document defines the deployment architecture for Nimbus.

It covers:

* Frontend deployment
* Backend deployment
* Machine Learning deployment
* Database deployment
* File storage
* CI/CD
* Environment variables
* Domains
* SSL
* Monitoring
* Logging
* Production releases
* Disaster recovery

---

# 2. Deployment Architecture

```text id="6jxmwd"
                    Internet
                        │
                        ▼
                Cloudflare DNS (Future)
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
 Next.js Frontend                 FastAPI Backend
     (Vercel)                        (Render)
        │                               │
        ├──────────────┬────────────────┤
        │              │                │
        ▼              ▼                ▼
   Supabase DB   Object Storage   AI Providers
  (PostgreSQL)    (Supabase)    (OpenAI/Gemini)
                        │
                        ▼
                Machine Learning Models
```

---

# 3. Services

| Component      | Provider                 |
| -------------- | ------------------------ |
| Frontend       | Vercel                   |
| Backend        | Render                   |
| Database       | Supabase PostgreSQL      |
| Authentication | JWT (FastAPI)            |
| Storage        | Supabase Storage         |
| Source Control | GitHub                   |
| CI/CD          | GitHub Actions           |
| Monitoring     | Render + Sentry (Future) |
| Analytics      | PostHog (Future)         |

---

# 4. Frontend Deployment

Framework:

Next.js 15

Platform:

Vercel

Root Directory:

```text id="u4q6g8"
frontend/
```

Build Command:

```text id="ywkhv3"
pnpm build
```

Output:

Managed automatically by Next.js.

---

# 5. Backend Deployment

Framework:

FastAPI

Platform:

Render

Root Directory:

```text id="yap5d2"
backend/
```

Start Command:

```text id="3ryjlwm"
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Python Version:

```text id="k73drm"
3.14
```

---

# 6. Database Deployment

Provider:

Supabase

Engine:

PostgreSQL 17

Responsibilities:

* User data
* Products
* Inventory
* Forecasts
* Analytics
* Business data
* Audit logs

---

# 7. Object Storage

Provider:

Supabase Storage

Stores:

* CSV uploads
* Product images
* Company logos
* Exported reports
* Model artifacts (optional)

Large files should not be stored in PostgreSQL.

---

# 8. Environment Variables

## Frontend

```text id="5chazm"
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

---

## Backend

```text id="zcd7t7"
DATABASE_URL=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

JWT_SECRET_KEY=
JWT_ALGORITHM=

OPENAI_API_KEY=
GOOGLE_API_KEY=

REDIS_URL=

ENVIRONMENT=
```

Never commit secrets to Git.

Commit only:

```text id="zwr1v3"
.env.example
```

---

# 9. Domain Structure

Production:

```text id="fjm5d8"
www.nimbus-ai.com
```

Frontend API calls:

```text id="2kndy6"
api.nimbus-ai.com
```

Future Admin:

```text id="zhdcgf"
admin.nimbus-ai.com
```

Future Docs:

```text id="qmtnmb"
docs.nimbus-ai.com
```

---

# 10. HTTPS

All production traffic must use HTTPS.

Enable automatic SSL certificates.

Redirect HTTP → HTTPS.

---

# 11. CI/CD Pipeline

Workflow:

```text id="98mjwr"
Push to GitHub

↓

Run Tests

↓

Lint

↓

Build

↓

Deploy Frontend

↓

Deploy Backend

↓

Run Database Migration

↓

Health Check
```

Deployments should stop if any mandatory step fails.

---

# 12. Git Branch Strategy

```text id="pp4g1d"
main

development

feature/*
```

Rules:

* `main` is always deployable.
* Feature branches require pull requests.
* Development is the integration branch.

---

# 13. Database Migrations

Use:

Alembic

Every schema change must:

* Create a migration.
* Be reviewed.
* Be committed to Git.
* Be applied automatically during deployment.

Never edit production tables manually.

---

# 14. Health Checks

Endpoint:

```text id="qllpvw"
/api/v1/health
```

Checks:

* API
* Database
* ML service
* Storage
* AI provider connectivity (non-blocking where appropriate)

---

# 15. Logging

Application logs:

* Requests
* Errors
* Warnings
* Authentication events
* Forecast generation
* CSV uploads

Avoid logging passwords, tokens, or sensitive business data.

---

# 16. Monitoring

Track:

* API uptime
* Response times
* Database latency
* Memory usage
* CPU usage
* Forecast generation time
* Failed jobs
* Error rates

Future:

* Sentry
* PostHog
* Grafana

---

# 17. Backup Strategy

Database:

* Automated daily backups.
* Point-in-time recovery when supported.

Storage:

* Versioned backups for important assets.

Test restoration procedures periodically.

---

# 18. Rollback Strategy

If deployment fails:

1. Stop new traffic.
2. Roll back to the previous application version.
3. Restore database only if required by the migration strategy.
4. Verify health checks.
5. Resume traffic.

---

# 19. Scaling Strategy

### Frontend

Scale automatically through Vercel.

### Backend

Upgrade Render instance or introduce multiple instances behind a load balancer when needed.

### Database

Optimize queries, add indexes, and consider read replicas before major architectural changes.

### ML

Separate the inference service if forecasting load grows significantly.

---

# 20. Security

Production requirements:

* HTTPS only
* Secure environment variables
* Principle of least privilege
* Database row isolation by `business_id`
* Regular dependency updates
* Rate limiting
* Security headers
* Input validation

---

# 21. Production Release Checklist

Before every release:

* All tests pass.
* Lint passes.
* Database migrations reviewed.
* Environment variables verified.
* Health endpoint passes.
* No critical security issues.
* Documentation updated.
* Release notes prepared.

---

# 22. Future Improvements

As Nimbus scales, consider:

* Cloudflare CDN
* Redis caching
* Background job workers
* Dedicated ML inference service
* Kubernetes deployment
* Object storage CDN
* Blue-Green deployments
* Canary releases
* Multi-region infrastructure

---

# 23. Definition of Done

Nimbus deployment is considered production-ready when:

* Frontend is deployed to Vercel.
* Backend is deployed to Render.
* Database is hosted on Supabase.
* Storage is configured.
* CI/CD is automated.
* Environment variables are secured.
* HTTPS is enforced.
* Health checks pass.
* Monitoring is active.
* Backup strategy is documented.
* Rollback procedure is validated.

# Docker & Containerization Strategy

## Purpose

Nimbus uses Docker to ensure that every development, testing, and production environment runs the application with the same dependencies and configuration.

Containerization improves:

* Development consistency
* Dependency management
* Deployment reliability
* CI/CD automation
* Scalability
* Portability

Docker is considered part of the core deployment architecture.

---

# 1. Container Architecture

```text
                     Docker Network
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Backend API          ML Service         Redis (Future)
  FastAPI             Python ML
        │                  │
        └──────────┬───────┘
                   ▼
          Supabase PostgreSQL
```

The frontend remains deployed independently on Vercel.

---

# 2. Containers

Nimbus initially consists of the following containers:

## Backend

Responsibilities

* REST API
* Authentication
* Business Logic
* Database Access
* AI Integration

Technology

* FastAPI
* SQLAlchemy
* Alembic

---

## ML Service

Responsibilities

* Model Loading
* Forecast Generation
* Inventory Optimization
* Model Evaluation

Technology

* Python
* XGBoost
* Prophet
* Pandas
* Scikit-learn

---

## Redis (Future)

Responsibilities

* Caching
* Background Jobs
* Rate Limiting
* Session Storage (optional)

Initially optional.

---

# 3. Project Structure

```text
Nimbus/

frontend/

backend/
├── Dockerfile

ml/
├── Dockerfile

docker-compose.yml

.env.example
```

---

# 4. Backend Dockerfile

The backend image should:

* Use Python 3.14
* Install dependencies
* Copy application source
* Expose the application port
* Start FastAPI using Uvicorn

The Dockerfile should remain lightweight and use multi-stage builds if future optimization is required.

---

# 5. ML Dockerfile

The ML image should:

* Use Python 3.14
* Install ML dependencies
* Copy trained model artifacts when required
* Expose the inference service
* Support future background workers

The ML container should remain independent from the API container.

---

# 6. Docker Compose

The local development environment should be orchestrated using Docker Compose.

Services:

* backend
* ml
* redis (future)

Supabase remains an external managed service.

---

# 7. Development Workflow

Typical workflow:

```text
Developer

↓

Pull Repository

↓

Copy .env.example → .env

↓

docker compose up

↓

Backend Running

↓

ML Running

↓

Begin Development
```

Developers should not need to install Python packages manually outside the containers.

---

# 8. Environment Variables

Containers receive configuration through environment variables.

Sensitive values must never be baked into images.

Use:

* `.env` (local)
* Render environment variables (production)
* GitHub Secrets (CI/CD)

---

# 9. Networking

Backend communicates with:

* Supabase
* AI providers
* ML service

ML service communicates with:

* Model artifacts
* Backend (when required)

All container communication should occur over an internal Docker network during local development.

---

# 10. CI/CD Integration

Every backend change should:

1. Build Docker image.
2. Run tests.
3. Perform linting.
4. Build successfully.
5. Deploy to production.

Image build failures must block deployment.

---

# 11. Image Versioning

Recommended tags:

```text
backend:1.0.0
backend:1.0.1
backend:1.1.0

ml:1.0.0
ml:1.0.1
```

Avoid relying on the `latest` tag for production deployments.

---

# 12. Security

Container images should:

* Use minimal base images where practical.
* Run as a non-root user when possible.
* Exclude unnecessary build tools.
* Avoid embedding secrets.
* Be rebuilt regularly to receive security updates.

---

# 13. Future Container Expansion

As Nimbus grows, additional services may be containerized:

* Background Worker
* Scheduler
* Notification Service
* OCR Service
* Analytics Service
* Monitoring Stack

The architecture is designed so these services can be introduced without disrupting existing deployments.

---

# 14. Engineering Decision

Docker is the standard execution environment for Nimbus.

All backend and machine learning components should be developed with containerization in mind, ensuring consistent behavior across local development, testing, CI/CD, and production.
