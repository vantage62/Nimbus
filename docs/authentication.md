# Authentication & Authorization Design

**Project:** Nimbus
**Version:** 1.0.0
**Status:** Production Design

---

# 1. Purpose

This document defines the authentication and authorization architecture for Nimbus.

It specifies:

* User authentication
* Authorization
* JWT implementation
* Role-Based Access Control (RBAC)
* Session management
* Password security
* Token lifecycle
* Protected API access
* Security best practices

This document is the single source of truth for all authentication-related functionality.

---

# 2. Authentication Goals

Nimbus authentication must:

* Secure user accounts.
* Support multiple businesses (multi-tenant SaaS).
* Isolate business data.
* Use industry-standard security practices.
* Scale to thousands of users.
* Integrate seamlessly with the FastAPI backend.

---

# 3. Authentication Architecture

```text
User
   │
   ▼
Next.js Frontend
   │
   ▼
Login API
   │
   ▼
FastAPI Backend
   │
   ▼
Password Verification
   │
   ▼
JWT Generation
   │
   ▼
Access Token + Refresh Token
   │
   ▼
Protected API Requests
```

---

# 4. Authentication Flow

### User Registration

1. User submits registration form.
2. Backend validates input.
3. Password is hashed.
4. Business is created.
5. Administrator account is created.
6. JWT tokens are issued.
7. User is authenticated.

---

### User Login

1. User submits email and password.
2. Backend validates credentials.
3. Password hash is verified.
4. Access token generated.
5. Refresh token generated.
6. Tokens returned to frontend.

---

### Authenticated Request

1. Frontend sends:

```http
Authorization: Bearer <access_token>
```

2. Backend validates token.
3. Backend extracts:

* User ID
* Business ID
* User Role

4. Request proceeds.

---

### Token Expiration

When the access token expires:

1. Frontend sends refresh token.
2. Backend validates refresh token.
3. New access token generated.
4. Old refresh token remains valid until expiry (or is rotated in future versions).

---

# 5. User Roles

Nimbus uses Role-Based Access Control (RBAC).

Roles:

## Admin

Permissions:

* Full system access
* Manage users
* Manage inventory
* Manage business settings
* Generate forecasts
* Manage products
* Upload CSV
* View analytics
* Configure notifications

---

## Manager

Permissions:

* Manage inventory
* Manage products
* Upload CSV
* Generate forecasts
* View analytics
* View notifications
* Update inventory

Cannot:

* Manage business owners
* Delete business
* Change subscription settings

---

## Employee

Permissions:

* View dashboard
* View inventory
* View products
* View notifications

Cannot:

* Upload CSV
* Generate forecasts
* Delete data
* Change settings
* Manage users

---

# 6. Permission Matrix

| Feature          | Admin | Manager |  Employee |
| ---------------- | :---: | :-----: | :-------: |
| Dashboard        |   ✅   |    ✅    |     ✅     |
| Inventory        |   ✅   |    ✅    |     ✅     |
| Products         |   ✅   |    ✅    |     ✅     |
| CSV Upload       |   ✅   |    ✅    |     ❌     |
| Forecasting      |   ✅   |    ✅    |     ❌     |
| Analytics        |   ✅   |    ✅    | View Only |
| Notifications    |   ✅   |    ✅    |     ✅     |
| Settings         |   ✅   | Limited |     ❌     |
| User Management  |   ✅   |    ❌    |     ❌     |
| Business Profile |   ✅   |    ❌    |     ❌     |

---

# 7. JWT Design

Nimbus uses two tokens.

## Access Token

Purpose:

Authenticate API requests.

Contains:

* User ID
* Business ID
* Role
* Token ID
* Issued At
* Expiration

Lifetime:

15 minutes

---

## Refresh Token

Purpose:

Generate new access tokens.

Lifetime:

7 days

Future versions may support configurable durations.

---

# 8. JWT Payload

Example:

```json
{
  "sub": "user_uuid",
  "business_id": "business_uuid",
  "role": "admin",
  "iat": 1725000000,
  "exp": 1725000900,
  "jti": "token_uuid"
}
```

---

# 9. Password Policy

Minimum requirements:

* At least 8 characters
* At least one uppercase letter
* At least one lowercase letter
* At least one number
* At least one special character

Passwords should never be stored or logged in plain text.

---

# 10. Password Hashing

Algorithm:

Argon2id (preferred)

Fallback:

bcrypt

Requirements:

* Unique salt per password
* Strong work factor
* Constant-time verification

---

# 11. Multi-Tenant Authorization

Every authenticated user belongs to one business.

Every protected database query must include:

```sql
WHERE business_id = current_user.business_id
```

Business isolation is mandatory.

Cross-business access must never be possible.

---

# 12. Session Management

Active sessions should include:

* User ID
* Device (future)
* Login timestamp
* Last activity
* Refresh token status

Future releases may support viewing and revoking active sessions.

---

# 13. Logout

Logout process:

1. Frontend deletes access token.
2. Refresh token is invalidated (future enhancement).
3. User session ends.

---

# 14. Protected Routes

Examples:

Protected:

* Dashboard
* Inventory
* Products
* Forecasting
* Analytics
* Settings
* Notifications
* Business Profile
* AI Chat

Public:

* Login
* Register
* Refresh Token
* Health Check

---

# 15. Authorization Middleware

Every protected request should:

1. Validate JWT.
2. Verify token expiration.
3. Extract user identity.
4. Verify business membership.
5. Verify required role.
6. Continue request.

Unauthorized requests return:

```http
401 Unauthorized
```

Forbidden requests return:

```http
403 Forbidden
```

---

# 16. Security Headers

The backend should enforce:

* HTTPS
* HSTS
* X-Content-Type-Options
* X-Frame-Options
* Referrer-Policy
* Content-Security-Policy (where applicable)

---

# 17. Rate Limiting

Recommended defaults:

Login:

* 5 attempts per minute per IP

Registration:

* 3 requests per minute per IP

Refresh Token:

* 10 requests per minute

General API:

* 120 requests per minute

AI Chat:

* 30 requests per minute

---

# 18. Failed Login Protection

After repeated failed logins:

* Temporary account lock (recommended)
* Progressive delay between attempts
* Security event logged

Future versions may include CAPTCHA after excessive failures.

---

# 19. Audit Logging

Security-related events should be logged:

* Registration
* Login
* Logout
* Password change
* Password reset
* Failed login
* Token refresh
* Role changes

Logs must never contain passwords or tokens.

---

# 20. Password Reset

Flow:

1. User requests reset.
2. Secure reset token generated.
3. Email sent.
4. User sets new password.
5. Existing sessions invalidated (recommended).
6. New login required.

---

# 21. Email Verification

Future enhancement:

1. User registers.
2. Verification email sent.
3. Verification link clicked.
4. Account activated.

---

# 22. Future Authentication Features

Planned improvements:

* Two-Factor Authentication (2FA)
* Passkeys (WebAuthn)
* Single Sign-On (Google, Microsoft)
* Device management
* Session revocation
* Login history
* Trusted devices
* IP-based anomaly detection

---

# 23. Environment Variables

Required:

```text
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_HASH_ALGORITHM=argon2id
```

Additional secrets:

```text
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
```

Never commit `.env` files.

Only commit `.env.example`.

---

# 24. Authentication Testing

Critical test cases:

* Successful registration
* Successful login
* Invalid credentials
* Expired access token
* Invalid refresh token
* Role authorization
* Business isolation
* Password hashing verification
* Token expiration
* Logout flow

---

# 25. Security Principles

Nimbus authentication follows these principles:

* Zero Trust Architecture
* Least Privilege Access
* Defense in Depth
* Secure by Default
* Principle of Least Exposure
* Multi-Tenant Isolation
* Token-Based Authentication
* Strong Password Security

---

# 26. Definition of Done

The authentication system is considered production-ready when:

* User registration works correctly.
* Login and logout function reliably.
* Passwords are securely hashed.
* JWT authentication protects all private endpoints.
* Refresh token flow works correctly.
* Role-based authorization is enforced.
* Business data isolation is guaranteed.
* Security events are logged.
* Automated authentication tests pass.
* All authentication APIs are documented and versioned.

---

# 27. Future Migration Strategy

As Nimbus grows, authentication can evolve without breaking existing clients.

Planned evolution:

**Phase 1 (MVP)**

* JWT Authentication
* RBAC
* Refresh Tokens

**Phase 2**

* Email Verification
* Password Reset Emails
* Session Tracking

**Phase 3**

* Two-Factor Authentication (2FA)
* OAuth Providers (Google/Microsoft)
* Trusted Devices

**Phase 4**

* WebAuthn / Passkeys
* Enterprise SSO
* Advanced Security Analytics

The authentication architecture is intentionally modular so that these capabilities can be added with minimal changes to existing APIs and frontend workflows.

# Database Enhancement — Authentication & Session Management

This section extends the database design to support secure authentication, session management, and future enterprise security features.

---

# 1. Update to `users` Table

The existing `users` table should be extended with the following authentication-related fields.

| Column                | Type              | Description                                                          |
| --------------------- | ----------------- | -------------------------------------------------------------------- |
| email_verified_at     | TIMESTAMP NULL    | Timestamp when the user's email address was verified.                |
| last_login_at         | TIMESTAMP NULL    | Stores the user's most recent successful login.                      |
| failed_login_attempts | INTEGER DEFAULT 0 | Tracks consecutive failed login attempts.                            |
| account_locked_until  | TIMESTAMP NULL    | Prevents login until this time if the account is temporarily locked. |
| password_changed_at   | TIMESTAMP NULL    | Records the last password change.                                    |

Updated structure (authentication-related fields only):

```text
users

id
business_id
first_name
last_name
email
password_hash

email_verified_at
last_login_at
failed_login_attempts
account_locked_until
password_changed_at

role
phone
is_active

created_at
updated_at
deleted_at
```

---

# 2. New Table — `refresh_tokens`

Purpose

Nimbus uses JWT Access Tokens together with Refresh Tokens.

Refresh tokens should **never** be stored in plain text.

Instead, only a secure hash of the refresh token is stored.

This allows:

* Secure logout
* Session revocation
* Device management
* "Logout from all devices"
* Token rotation
* Session tracking

---

## Table Structure

```text
refresh_tokens

id
user_id
token_hash

expires_at
revoked_at

device_name
ip_address
user_agent

created_at
updated_at
```

---

## Columns

### id

UUID

Primary Key

---

### user_id

UUID

Foreign Key

References

users.id

---

### token_hash

TEXT

Stores the hashed refresh token.

Never store the original refresh token.

---

### expires_at

TIMESTAMP

Expiration timestamp.

---

### revoked_at

TIMESTAMP NULL

NULL indicates an active token.

If populated, the token is no longer valid.

---

### device_name

VARCHAR(255)

Examples:

* Chrome on Windows
* Edge on Windows
* Safari on iPhone

Optional for the MVP.

---

### ip_address

INET

IP address used when the session was created.

Useful for security auditing.

---

### user_agent

TEXT

Browser or application information.

Useful for future "Trusted Devices" functionality.

---

### created_at

TIMESTAMP

Creation timestamp.

---

### updated_at

TIMESTAMP

Last modification timestamp.

---

# 3. Relationships

```text
Business
    │
    ▼
Users
    │
    ▼
Refresh Tokens
```

One User

↓

Many Refresh Tokens

---

# 4. Login Flow

```text
User Login

↓

Verify Password

↓

Generate Access Token

↓

Generate Refresh Token

↓

Hash Refresh Token

↓

Store Hash

↓

Return Original Refresh Token
```

---

# 5. Logout Flow

```text
User Logout

↓

Find Refresh Token

↓

Set revoked_at

↓

Access Token Expires Naturally
```

---

# 6. Refresh Flow

```text
Refresh Token

↓

Hash Incoming Token

↓

Compare Hash

↓

Check Expiration

↓

Check Revoked

↓

Generate New Access Token

↓

(Optional) Rotate Refresh Token
```

---

# 7. Token Rotation (Future)

Future versions should support Refresh Token Rotation.

Flow

```text
Refresh Request

↓

Old Refresh Token Revoked

↓

New Refresh Token Generated

↓

Store New Hash

↓

Return New Token
```

This prevents replay attacks.

---

# 8. Account Lock Protection

If login attempts exceed the configured threshold:

```text
failed_login_attempts += 1

↓

If attempts exceed threshold

↓

account_locked_until = NOW + 15 minutes
```

Successful login resets:

```text
failed_login_attempts = 0
```

---

# 9. Email Verification

Workflow

```text
Register

↓

Create User

↓

Generate Verification Token

↓

Send Email

↓

Verify Email

↓

email_verified_at = CURRENT_TIMESTAMP
```

---

# 10. Password Changes

Whenever a password is updated:

```text
password_changed_at = CURRENT_TIMESTAMP
```

Existing sessions may optionally be revoked for enhanced security.

---

# 11. Future Security Enhancements

This design supports future implementation of:

* Two-Factor Authentication (2FA)
* Passkeys (WebAuthn)
* Google OAuth
* Microsoft OAuth
* Device Management
* Login History
* Session Management
* Enterprise SSO
* Risk-Based Authentication

without requiring major database changes.

---

# 12. Engineering Decision

Nimbus intentionally separates:

* User identity (`users`)
* Authentication credentials (`password_hash`)
* Session management (`refresh_tokens`)

This separation improves security, scalability, and maintainability.

The architecture aligns with modern SaaS authentication practices and provides a strong foundation for enterprise-grade identity management.

# Database Enhancement — Login History & Security Auditing

This section introduces the `login_history` table, which provides a permanent audit trail of authentication events.

Although optional for the MVP, it is strongly recommended as part of the core database design because it improves security, monitoring, debugging, and future enterprise readiness.

---

# 1. Purpose

The `login_history` table records every authentication attempt made against Nimbus.

Unlike `refresh_tokens`, which stores active sessions, `login_history` stores immutable historical records.

Each login attempt creates a new record.

Existing records are **never updated or deleted** except for appending logout information when applicable.

---

# 2. Table Structure

```text
login_history

id
business_id
user_id

login_time
logout_time

login_status
failure_reason

ip_address
user_agent
device_name

country
city

session_id

created_at
```

---

# 3. Columns

### id

UUID

Primary Key.

---

### business_id

UUID

Foreign Key

References:

```text
businesses.id
```

---

### user_id

UUID

Foreign Key

References:

```text
users.id
```

Nullable for failed login attempts where the email does not match an existing user.

---

### login_time

TIMESTAMP

Time of the authentication attempt.

---

### logout_time

TIMESTAMP NULL

Time when the session ended.

Remains NULL if:

* user is still logged in
* browser crashed
* session expired

---

### login_status

ENUM

Values:

```text
SUCCESS

FAILED

LOCKED

TOKEN_REFRESH

LOGOUT
```

---

### failure_reason

TEXT NULL

Examples:

* Invalid password
* User not found
* Account locked
* Expired token
* Revoked refresh token

Only populated when appropriate.

---

### ip_address

INET

IP address used during login.

Useful for anomaly detection.

---

### user_agent

TEXT

Stores browser or application information.

Example:

```text
Chrome 140 on Windows 11
```

---

### device_name

VARCHAR(255)

Friendly device description.

Examples:

* Office Laptop
* Home Desktop
* Android Phone
* iPhone

Initially populated automatically where possible.

Users may rename devices in future versions.

---

### country

VARCHAR(100)

Derived from IP geolocation.

Optional.

---

### city

VARCHAR(100)

Derived from IP geolocation.

Optional.

---

### session_id

UUID

Links authentication events together.

Allows tracking:

* Login
* Refresh
* Logout

within a single session.

---

### created_at

TIMESTAMP

Audit timestamp.

---

# 4. Relationships

```text
Business
     │
     ▼
Users
     │
     ▼
Login History
```

Relationship:

One User

↓

Many Login Events

---

# 5. Authentication Lifecycle

```text
User Login
      │
      ▼
Credentials Verified
      │
      ▼
Create Login History Record
      │
      ▼
Generate JWT
      │
      ▼
Create Refresh Token
      │
      ▼
Return Tokens
```

---

# 6. Logout Lifecycle

```text
Logout

↓

Revoke Refresh Token

↓

Update logout_time

↓

Session Closed
```

---

# 7. Failed Login Flow

```text
Login Attempt

↓

Password Incorrect

↓

failed_login_attempts++

↓

Insert FAILED Login History Record

↓

Return 401
```

---

# 8. Account Lock Flow

```text
Too Many Failed Attempts

↓

account_locked_until Updated

↓

Insert LOCKED Record

↓

Return 403
```

---

# 9. Security Benefits

The login history table enables:

* Login history dashboard
* Suspicious login detection
* New device detection
* Multiple device tracking
* Security investigations
* Enterprise audit logging
* Compliance reporting
* Future anomaly detection

---

# 10. Future Features Enabled

The table supports future implementation of:

* "Recent Login Activity"
* Email alerts for new logins
* Login notifications
* Device management
* Trusted devices
* Geographic login maps
* Impossible travel detection
* Risk scoring
* Enterprise compliance reports

without modifying the core authentication architecture.

---

# 11. Retention Policy

Recommended policy:

* Keep login history for a minimum of 365 days.
* Archive older records if necessary.
* Never delete records that are required for legal or compliance purposes.

---

# 12. Engineering Decision

Nimbus separates authentication into three distinct concerns:

### Users

Identity and profile information.

### Refresh Tokens

Active authenticated sessions.

### Login History

Permanent audit log of authentication events.

This separation improves maintainability, security, scalability, and observability while aligning the platform with enterprise SaaS design principles.

# Database Enhancement — Role-Based Access Control (RBAC)

This document extends the Nimbus authentication system by introducing a scalable Role-Based Access Control (RBAC) model.

Instead of hardcoding permissions into application logic, every action is controlled through database-managed permissions.

This architecture supports custom roles, enterprise deployments, and future feature expansion without requiring backend code changes.

---

# 1. RBAC Architecture

```text
Users
   │
   ▼
Roles
   │
   ▼
Role Permissions
   │
   ▼
Permissions
```

A user belongs to one role.

A role contains many permissions.

A permission can belong to many roles.

This forms a many-to-many relationship between roles and permissions.

---

# 2. Design Goals

The RBAC system must:

* Support unlimited custom roles.
* Support fine-grained permissions.
* Avoid hardcoded authorization logic.
* Allow future enterprise features.
* Support organization-specific role customization.
* Integrate with JWT authentication.

---

# 3. Database Tables

The RBAC system introduces three new tables:

```text
roles
permissions
role_permissions
```

The existing `users` table will reference the `roles` table instead of storing a plain role string.

---

# 4. Update to `users`

Replace:

```text
role
```

With:

```text
role_id
```

Relationship:

```text
Users
    │
    ▼
Roles
```

---

# 5. roles Table

Purpose:

Represents a collection of permissions.

Structure:

```text
roles

id
business_id
name
description
is_system_role

created_at
updated_at
deleted_at
```

---

### id

UUID

Primary Key.

---

### business_id

UUID

Allows businesses to create custom roles.

NULL indicates a built-in system role.

---

### name

Examples:

* Administrator
* Manager
* Employee
* Warehouse Supervisor
* Sales Executive

---

### description

Human-readable explanation.

---

### is_system_role

Boolean

TRUE

Cannot be deleted.

FALSE

Custom role.

---

# 6. permissions Table

Purpose:

Defines every action available in Nimbus.

Structure:

```text
permissions

id
name
module
description

created_at
```

---

Examples

```text
inventory.read
inventory.write
inventory.delete

products.read
products.create
products.update
products.delete

forecast.generate

analytics.view

chat.use

notifications.read

users.manage

settings.update

business.manage
```

Permissions should be immutable once released.

---

# 7. role_permissions Table

Purpose:

Maps roles to permissions.

Structure:

```text
role_permissions

role_id
permission_id

created_at
```

Composite Primary Key:

```text
(role_id, permission_id)
```

---

# 8. Relationships

```text
Users
   │
   ▼
Roles
   │
   ▼
Role Permissions
   │
   ▼
Permissions
```

---

# 9. Default System Roles

Nimbus ships with three predefined roles.

## Administrator

Permissions:

* All permissions.

---

## Manager

Permissions:

* Inventory
* Products
* Forecasting
* Analytics
* Notifications

Cannot:

* Delete business
* Manage roles
* Manage billing

---

## Employee

Permissions:

* View inventory
* View dashboard
* View products
* Read notifications

Cannot:

* Upload CSV
* Generate forecasts
* Manage users
* Update settings

---

# 10. Permission Naming Convention

Every permission follows:

```text
module.action
```

Examples:

```text
inventory.read
inventory.update
inventory.delete

products.create

forecast.generate

analytics.export

settings.update

users.invite
```

This convention keeps permissions predictable and easy to maintain.

---

# 11. Authorization Flow

```text
User Request
      │
      ▼
Validate JWT
      │
      ▼
Load User
      │
      ▼
Load Role
      │
      ▼
Load Permissions
      │
      ▼
Permission Check
      │
      ▼
Allow / Deny
```

---

# 12. JWT Integration

JWT should contain:

```json
{
    "sub": "user_uuid",
    "business_id": "business_uuid",
    "role_id": "role_uuid"
}
```

Permissions are loaded from the database during authorization.

Avoid embedding large permission lists inside JWTs, as they become stale if roles change.

---

# 13. FastAPI Authorization

Example:

```python
@router.post("/forecast")
@require_permission("forecast.generate")
```

The authorization dependency checks whether the authenticated user's role includes the required permission.

---

# 14. Custom Roles

Businesses may create roles such as:

* Store Manager
* Procurement Officer
* Inventory Controller
* Finance Officer
* Sales Analyst
* Warehouse Supervisor
* Auditor

No backend changes are required to support new roles.

---

# 15. Future Enterprise Features

This design enables:

* Department-based permissions
* Temporary permissions
* Time-limited access
* Approval workflows
* Role templates
* Permission groups
* Enterprise SSO mapping
* Compliance auditing

---

# 16. Recommended Seed Permissions

### Dashboard

* dashboard.view

### Products

* products.read
* products.create
* products.update
* products.delete

### Inventory

* inventory.read
* inventory.update
* inventory.adjust
* inventory.delete

### Forecasting

* forecast.generate
* forecast.read
* forecast.delete

### CSV

* csv.upload
* csv.history

### Analytics

* analytics.view
* analytics.export

### Notifications

* notifications.read
* notifications.manage

### AI

* chat.use
* voice.use

### Business

* business.read
* business.update

### Users

* users.read
* users.create
* users.update
* users.delete

### Roles

* roles.read
* roles.create
* roles.update
* roles.delete

### Settings

* settings.read
* settings.update

---

# 17. Engineering Principles

* Permissions are the source of truth.
* Roles are collections of permissions.
* Users receive permissions through roles.
* Authorization logic should never rely on hardcoded role names.
* New features introduce new permissions rather than new conditional statements.

---

# 18. Definition of Done

The RBAC system is considered complete when:

* Roles are stored in the database.
* Permissions are stored in the database.
* Role-to-permission mappings are implemented.
* Users are linked to roles.
* Every protected endpoint checks permissions.
* System roles are seeded automatically.
* Businesses can create custom roles.
* Authorization is fully database-driven.
