# Nimbus Engineering Principles

**Version:** 1.0.0
**Status:** Active

---

# 1. Purpose

This document defines the engineering standards for Nimbus.

Every contributor, whether human or AI, must follow these principles to ensure the codebase remains consistent, maintainable, secure, and scalable.

When in doubt, this document takes precedence over personal coding preferences.

---

# 2. Engineering Philosophy

Nimbus is built with the following priorities:

1. Correctness before speed.
2. Simplicity before cleverness.
3. Readability before brevity.
4. Maintainability before optimization.
5. Security by default.
6. Scalability by design.
7. Modular architecture over monolithic code.

---

# 3. Core Principles

The project follows:

* SOLID Principles
* DRY (Don't Repeat Yourself)
* KISS (Keep It Simple, Stupid)
* Separation of Concerns
* Dependency Injection
* Composition over Inheritance
* Clean Architecture
* Repository Pattern
* Service Layer Pattern

---

# 4. Monorepo Rules

Repository structure:

```text
nimbus/
├── frontend/
├── backend/
├── ml/
├── database/
├── docs/
├── scripts/
└── .github/
```

Rules:

* Frontend must never contain backend logic.
* Backend must never contain frontend code.
* ML training must remain independent of the API.
* Shared documentation belongs in `docs/`.
* Database schema changes must be version-controlled.

---

# 5. Backend Architecture Rules

Every request must follow this path:

```text
Client
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Business logic belongs only in Services.

Database queries belong only in Repositories.

Routers should only:

* Validate requests
* Call services
* Return responses

---

# 6. File Naming

Use lowercase with underscores.

Examples:

```text
forecast_service.py
inventory_repository.py
product_schema.py
```

Do not use:

```text
ForecastService.py
InventoryRepo.py
helperFunctions.py
```

---

# 7. Variable Naming

Use descriptive names.

Good:

```python
forecast_result
inventory_level
recommended_quantity
```

Avoid:

```python
data
temp
value
obj
x
```

---

# 8. Function Rules

Each function should:

* Have one responsibility.
* Be small.
* Be testable.
* Return predictable values.
* Include type hints.
* Include a concise docstring.

Avoid functions longer than ~50 lines unless there is a strong reason.

---

# 9. Class Rules

Each class should have a single responsibility.

Example:

Good:

* ForecastService
* InventoryRepository
* NotificationService

Bad:

* InventoryManagerThatHandlesEverything

---

# 10. API Standards

Every endpoint must be:

* Versioned
* RESTful
* JSON-based
* Authenticated when required

Base path:

```text
/api/v1/
```

---

# 11. Standard API Response

Successful response:

```json
{
  "success": true,
  "message": "Forecast generated successfully",
  "data": {}
}
```

Error response:

```json
{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND"
}
```

Never return inconsistent response formats.

---

# 12. Error Handling

Use centralized exception handlers.

Do not expose:

* SQL errors
* Stack traces
* Secrets
* Internal implementation details

Log detailed errors internally.

Return user-friendly messages externally.

---

# 13. Logging Standards

Every request should log:

* Timestamp
* User ID (if authenticated)
* HTTP method
* Endpoint
* Status code
* Duration

Log levels:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

Sensitive information must never be logged.

---

# 14. Database Rules

Always use:

* UUID primary keys
* Foreign keys
* Indexes where appropriate
* Soft deletes
* Created timestamps
* Updated timestamps

Never execute raw SQL unless absolutely necessary.

Use SQLAlchemy ORM.

---

# 15. Authentication Rules

Passwords:

* Never stored in plain text.
* Always hashed.

Authentication:

* JWT Access Token
* Refresh Token

Authorization:

* Role-based access control.

Roles:

* Admin
* Manager
* Employee

---

# 16. Validation Rules

Validate:

* Request body
* Query parameters
* Path parameters
* Uploaded files

Never trust client input.

Use Pydantic models.

---

# 17. Configuration

No secrets inside code.

Use environment variables.

Examples:

```text
DATABASE_URL
JWT_SECRET
OPENAI_API_KEY
SUPABASE_URL
```

Commit only `.env.example`.

Never commit `.env`.

---

# 18. Dependency Rules

Use:

* `uv` for Python dependency management.
* Lock dependencies before production.
* Keep frontend and backend dependencies separate.
* Upgrade intentionally and test after upgrades.

---

# 19. Git Workflow

Protected branches:

* `main`
* `develop`

Feature branches:

```text
feature/dashboard
feature/inventory
feature/forecasting
```

Bug fixes:

```text
bugfix/login
bugfix/csv-upload
```

Hotfixes:

```text
hotfix/security-patch
```

Never commit directly to `main`.

---

# 20. Commit Convention

Use Conventional Commits.

Examples:

```text
feat(api): add forecast endpoint
feat(ui): create inventory dashboard
fix(auth): resolve JWT validation
refactor(service): simplify inventory logic
docs: update API documentation
test(api): add forecast endpoint tests
chore: upgrade dependencies
```

---

# 21. Testing Standards

Every feature should include tests.

Minimum:

* Unit Tests
* Integration Tests

Critical features:

* Authentication
* Forecasting
* Inventory
* CSV Upload

Target:

* High confidence for business-critical logic.

---

# 22. Documentation Rules

Every public function should include a docstring.

Every module should explain its purpose.

Complex business rules should be documented.

API changes must update `docs/api.md`.

Database changes must update `docs/database.md`.

---

# 23. Code Review Checklist

Before merging:

* Builds successfully.
* Tests pass.
* Linting passes.
* Formatting passes.
* Type checking passes.
* Documentation updated.
* No secrets committed.
* No duplicated logic.
* Naming conventions followed.

---

# 24. Performance Principles

Optimize only after measuring.

Avoid:

* Premature optimization.
* N+1 database queries.
* Repeated model loading.
* Unnecessary API calls.

Cache expensive operations when appropriate.

---

# 25. Security Principles

Use HTTPS.

Validate all inputs.

Escape user-generated content.

Use parameterized queries.

Protect sensitive routes.

Rotate secrets when necessary.

Apply least-privilege access.

---

# 26. AI Development Guidelines

When generating code with AI:

* Generate one feature at a time.
* Follow the architecture document.
* Follow this engineering document.
* Do not invent new patterns.
* Do not duplicate existing functionality.
* Prefer extending existing modules over creating new ones.
* Keep code modular and production-ready.

---

# 27. Definition of Production-Ready

A feature is considered production-ready only if:

* Business logic is implemented.
* Tests are written and passing.
* Logging is included.
* Error handling is complete.
* Validation is implemented.
* Documentation is updated.
* Security considerations are addressed.
* The feature integrates cleanly with the existing architecture.

---

# 28. Decision-Making Principles

When multiple implementations are possible:

1. Prefer readability.
2. Prefer maintainability.
3. Prefer consistency with the existing architecture.
4. Prefer simpler solutions.
5. Optimize only with evidence.

---

# 29. Engineering Goal

Nimbus should evolve into a platform where:

* New modules can be added without major refactoring.
* AI-generated code is consistent with human-written code.
* Every component has a clear responsibility.
* The architecture remains understandable as the product grows.

These principles are mandatory for all future development.
