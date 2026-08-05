# Security Design Document

**Project:** Nimbus

**Version:** 1.0.0

**Status:** Production Security Specification

---

# 1. Purpose

This document defines the security architecture of Nimbus.

It establishes the policies, controls, and engineering practices required to protect user data, business information, machine learning assets, and application infrastructure.

---

# 2. Security Objectives

Nimbus must:

* Protect customer data.
* Ensure business isolation.
* Prevent unauthorized access.
* Secure API communication.
* Protect ML models.
* Secure uploaded files.
* Protect secrets.
* Maintain auditability.
* Support future compliance requirements.

---

# 3. Security Architecture

```text id="7bw7sh"
User
   │
HTTPS
   │
   ▼
Next.js Frontend
   │
JWT
   │
   ▼
FastAPI Backend
   │
   ├───────────────┐
   │               │
   ▼               ▼
Supabase      AI Providers
PostgreSQL    (OpenAI/Gemini)
   │
   ▼
Object Storage
```

Every layer is treated as potentially hostile and must validate all incoming data.

---

# 4. Authentication Security

Nimbus uses:

* JWT Access Tokens
* Refresh Tokens
* Argon2id password hashing
* Role-Based Access Control (RBAC)
* Multi-tenant authorization

Passwords are never stored in plain text.

Refresh tokens are stored as hashes.

---

# 5. Authorization

Every protected endpoint must verify:

1. JWT validity.
2. User existence.
3. Business membership.
4. Required permission.
5. Resource ownership where applicable.

Authorization decisions are permission-based, not role-name based.

---

# 6. Business Isolation

Every business owns its own data.

All database queries involving tenant-owned data must include:

```sql id="8jmfkk"
WHERE business_id = :current_business_id
```

Cross-business access is prohibited.

---

# 7. Transport Security

Production requirements:

* HTTPS only.
* Automatic HTTP → HTTPS redirects.
* Modern TLS versions.
* Secure cookies if cookies are introduced in future.

No sensitive data should be transmitted over unsecured connections.

---

# 8. Password Security

Requirements:

* Minimum 8 characters.
* Uppercase letter.
* Lowercase letter.
* Number.
* Special character.

Passwords are hashed using Argon2id.

Password comparisons must be constant-time.

---

# 9. Secrets Management

Secrets include:

* JWT secret
* Database credentials
* API keys
* Service tokens

Secrets must:

* Be stored in environment variables.
* Never be committed to Git.
* Be rotated periodically.

Only `.env.example` is committed.

---

# 10. File Upload Security

Nimbus supports CSV uploads.

Every uploaded file must be:

* Type validated.
* Size limited.
* Virus scanned (future).
* Parsed safely.
* Stored outside the database.

Reject:

* Executables
* Scripts
* Unsupported formats

---

# 11. Input Validation

Every request must be validated.

Validation includes:

* Required fields.
* Data types.
* Length limits.
* Numeric ranges.
* Date validation.
* Enum validation.

Use Pydantic models for request validation.

---

# 12. SQL Injection Protection

All database operations must use parameterized queries through SQLAlchemy.

Never concatenate SQL strings using user input.

---

# 13. Cross-Site Scripting (XSS)

Frontend must:

* Escape user-generated content.
* Sanitize rendered HTML.
* Avoid `dangerouslySetInnerHTML` unless absolutely necessary.

---

# 14. Cross-Site Request Forgery (CSRF)

The MVP uses JWT in the `Authorization` header, reducing CSRF risk.

If cookie-based authentication is introduced later, CSRF protection must be added.

---

# 15. Rate Limiting

Recommended limits:

* Login: 5 requests/minute
* Register: 3 requests/minute
* Forecast generation: 20 requests/minute
* AI chat: 30 requests/minute
* CSV upload: 10 requests/hour
* General API: 120 requests/minute

---

# 16. Logging

Log:

* Login attempts
* Permission denials
* Forecast generation
* CSV uploads
* Critical errors

Never log:

* Passwords
* JWTs
* Refresh tokens
* API keys

---

# 17. Audit Trail

Security events must be recorded using:

* `audit_logs`
* `login_history`

Critical events:

* Login
* Logout
* Role changes
* Password changes
* CSV uploads
* Forecast generation
* Permission changes

---

# 18. AI Security

AI responses must not:

* Execute code.
* Modify the database directly.
* Expose secrets.
* Reveal another business's data.

AI should only operate on data available to the authenticated business.

---

# 19. ML Security

Protect:

* Trained models
* Model metadata
* Training datasets

Only authorized users should trigger retraining or model replacement.

Model artifacts should be versioned and access-controlled.

---

# 20. API Security

Every endpoint must:

* Validate input.
* Return consistent error responses.
* Require authentication where appropriate.
* Enforce permissions.
* Use HTTPS.

---

# 21. Dependency Security

Dependencies should be:

* Pinned to compatible versions.
* Reviewed before upgrades.
* Updated regularly.

Use automated vulnerability scanning in CI when feasible.

---

# 22. Monitoring

Monitor:

* Failed logins
* Permission failures
* API errors
* Unusual request spikes
* Forecast failures
* Upload failures

Alerts should be generated for repeated or critical security events.

---

# 23. Backup & Recovery

Database:

* Automated backups.
* Verified restoration process.

Storage:

* Periodic backups for critical assets.

Document recovery procedures.

---

# 24. Incident Response

When a security incident occurs:

1. Detect.
2. Contain.
3. Investigate.
4. Recover.
5. Review.
6. Improve controls.

Post-incident documentation is required.

---

# 25. Future Security Enhancements

Planned:

* Two-Factor Authentication
* WebAuthn / Passkeys
* OAuth Providers
* Security Dashboard
* Device Management
* IP Reputation Checks
* Anomaly Detection
* WAF Integration
* DDoS Protection
* Automated Secret Rotation

---

# 26. Security Principles

Nimbus follows:

* Zero Trust
* Least Privilege
* Defense in Depth
* Secure by Default
* Principle of Least Exposure
* Multi-Tenant Isolation
* Continuous Monitoring

---

# 27. Definition of Done

Nimbus security is considered production-ready when:

* Authentication is secure.
* Authorization is permission-based.
* Business isolation is enforced.
* Secrets are protected.
* Uploaded files are validated.
* Inputs are validated.
* SQL injection risks are mitigated.
* Logs avoid sensitive data.
* Audit trails are complete.
* Recovery procedures are documented.
