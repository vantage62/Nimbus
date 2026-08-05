# Nimbus System Architecture

**Version:** 1.0.0
**Status:** Draft

---

# 1. Overview

Nimbus is a cloud-native AI-powered SaaS platform that enables retail businesses to predict demand, optimize inventory, and make data-driven business decisions.

The system follows a modular, service-oriented architecture with a clear separation between the frontend, backend, machine learning pipeline, and database.

The architecture prioritizes:

* Scalability
* Maintainability
* Security
* Modularity
* Explainability
* High performance

---

# 2. High-Level Architecture

```text
                        Internet
                            │
                    ┌───────▼────────┐
                    │    Vercel      │
                    │ Next.js Client │
                    └───────┬────────┘
                            │ HTTPS
                            ▼
                 api.nimbus-ai.com
                            │
                    ┌───────▼────────┐
                    │     Render     │
                    │ FastAPI Server │
                    └───────┬────────┘
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   Supabase DB      ML Inference Layer    AI Providers
 PostgreSQL             (Python)      (OpenAI/Gemini)
```

---

# 3. System Components

Nimbus consists of four major layers.

## Presentation Layer

Technology

* Next.js
* React
* TailwindCSS
* TypeScript

Responsibilities

* Authentication
* Dashboard
* Inventory UI
* Charts
* CSV Upload
* AI Chat Interface
* Voice Interface
* Settings
* Business Profile

The frontend never communicates directly with PostgreSQL.

---

## API Layer

Technology

* FastAPI

Responsibilities

* Authentication
* Authorization
* Business Logic
* Validation
* Inventory APIs
* Dashboard APIs
* Forecast APIs
* Notification APIs
* AI APIs

Every request from the frontend passes through the API.

---

## Machine Learning Layer

Technology

Python

Responsibilities

* Forecast generation
* Inventory optimization
* Feature engineering
* Model loading
* Prediction
* Confidence scoring

The ML layer is independent from the API layer.

The API requests predictions from the ML layer.

---

## Data Layer

Technology

Supabase PostgreSQL

Stores

Users

Businesses

Stores

Products

Inventory

Sales

Forecasts

Notifications

Settings

---

# 4. Deployment Architecture

Frontend

Hosted on Vercel

Backend

Hosted on Render

Database

Hosted on Supabase

ML

Runs within the backend process for MVP.

Future versions may separate ML into its own service.

---

# 5. Monorepo Structure

```text
nimbus/

.github/

docs/

frontend/

backend/

ml/

database/

scripts/

README.md
```

---

# 6. Backend Structure

```text
backend/

app/

api/

core/

database/

models/

schemas/

repositories/

services/

middleware/

utils/

tests/

main.py
```

Responsibilities

API

Receives requests.

Services

Business logic.

Repositories

Database communication.

Models

Database schema.

Schemas

Request/response validation.

Database

Connection and sessions.

Core

Configuration and security.

Middleware

Authentication, CORS, rate limiting.

---

# 7. Frontend Structure

```text
frontend/

app/

components/

hooks/

lib/

types/

public/
```

Responsibilities

Pages

Routing

Components

Reusable UI

Hooks

Business logic

Lib

API utilities

Types

Shared interfaces

---

# 8. ML Structure

```text
ml/

datasets/

preprocessing/

feature_engineering/

training/

evaluation/

models/

saved_models/

inference/
```

Responsibilities

Training

Model creation

Evaluation

Metrics

Inference

Predictions

Saved Models

Serialized trained models

---

# 9. Request Lifecycle

Example

Generate Forecast

1.

User clicks

Generate Forecast

↓

2.

Frontend sends

POST

/api/v1/forecast

↓

3.

Backend validates request

↓

4.

Forecast Service executes

↓

5.

Repository loads sales history

↓

6.

ML model predicts demand

↓

7.

Inventory optimizer calculates

Safety Stock

Reorder Point

Recommended Quantity

↓

8.

Forecast saved

↓

9.

Response returned

↓

10.

Dashboard updates

---

# 10. Communication Flow

Frontend

↓

REST API

↓

Service Layer

↓

Repository Layer

↓

Database

and

↓

ML Layer

↓

Response

---

# 11. Authentication Flow

Register

↓

Password Hash

↓

JWT Generated

↓

Frontend stores token securely

↓

Future requests

↓

Authorization Header

↓

Backend validates JWT

↓

Protected Route Access

---

# 12. API Design Principles

RESTful

Versioned

/api/v1/

JSON Responses

Consistent Error Format

Stateless

Authentication Required

Meaningful Status Codes

---

# 13. Business Modules

Nimbus contains the following modules.

Authentication

Dashboard

Inventory

Products

Sales

Forecasting

Analytics

Business Profile

Notifications

Settings

AI Chat

Voice Assistant

CSV Upload

Each module follows the same architecture.

Router

↓

Service

↓

Repository

↓

Database

---

# 14. Layer Responsibilities

Routers

Receive requests

Call services

Return responses

Never contain business logic.

---

Services

Business rules

Validation

ML integration

Notifications

Inventory calculations

---

Repositories

Database queries

CRUD

Filtering

Transactions

---

Models

Database representation

---

Schemas

Validation

Serialization

API contracts

---

# 15. Dependency Injection

FastAPI dependency injection will be used for:

Database sessions

Authenticated users

Repositories

Services

Configuration

---

# 16. Error Handling

Centralized exception handlers.

Standard response format.

Example

```json
{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND"
}
```

---

# 17. Logging

Every request should log:

Timestamp

Method

Endpoint

Execution Time

Status Code

Authenticated User

Errors

Logs should never expose sensitive information.

---

# 18. Security

JWT Authentication

Password Hashing

Input Validation

Rate Limiting

HTTPS Only

Environment Variables

SQL Injection Protection

CORS

Secure Headers

Soft Deletes

Audit Logging

---

# 19. Scalability

Nimbus is designed for horizontal scalability.

Frontend scales independently.

Backend scales independently.

Database can scale independently.

Future architecture may include:

Redis Cache

Background Workers

Message Queues

Dedicated ML Service

CDN

---

# 20. Guiding Principles

Every architectural decision should satisfy:

* Single Responsibility Principle
* SOLID Principles
* Repository Pattern
* Service Pattern
* Dependency Injection
* Loose Coupling
* High Cohesion
* Clear Module Boundaries
* Testability
* Security by Design

---

# 21. Architecture Decisions

### ADR-001

Use a monorepo for all services.

Reason:

Simpler development, easier versioning, centralized documentation, and synchronized deployments.

---

### ADR-002

Use FastAPI for the backend.

Reason:

High performance, automatic OpenAPI generation, excellent Python ecosystem support.

---

### ADR-003

Use Supabase PostgreSQL.

Reason:

Managed PostgreSQL, reliability, scalability, and strong SQL support.

---

### ADR-004

Use Vercel for the frontend.

Reason:

Native Next.js support, global CDN, preview deployments.

---

### ADR-005

Use Render for the backend.

Reason:

Simple deployment, Docker support, GitHub integration, and good Python compatibility.

---

### ADR-006

Keep ML separate from the API layer.

Reason:

The backend should consume predictions, not own the training pipeline. This separation simplifies experimentation, testing, and future scaling.

---

# 22. Future Architecture

As Nimbus grows, the architecture can evolve to:

* Dedicated ML inference service
* Scheduled model retraining workers
* Redis caching for frequent dashboard queries
* Background jobs for CSV processing and notifications
* WebSocket support for live dashboard updates
* ERP/POS integrations through adapter services
* Multi-region deployments for lower latency

The initial architecture is intentionally designed so these additions can be introduced without major refactoring.
