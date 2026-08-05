# Database Design Document

**Project:** Nimbus
**Version:** 1.0.0
**Database:** PostgreSQL (Supabase)

---

# 1. Purpose

This document defines the complete relational database architecture for Nimbus.

It serves as the single source of truth for:

* Database schema
* SQLAlchemy models
* Alembic migrations
* API development
* Backend repositories
* Future integrations

---

# 2. Database Philosophy

Nimbus is designed as a **multi-tenant SaaS application**.

This means:

* One database
* Multiple businesses
* Each business only accesses its own data
* All business-owned records are isolated using `business_id`

Every query in the backend must be scoped to the authenticated business.

---

# 3. Database Engine

Provider

Supabase

Engine

PostgreSQL 17

Extensions

* pgcrypto
* uuid-ossp (if required)
* pgvector (future AI features)

---

# 4. Design Principles

The database follows these principles:

* UUID primary keys
* Normalized schema (3NF)
* Foreign key integrity
* Soft deletes
* Audit timestamps
* Indexed search columns
* Cascade only where appropriate
* Explicit relationships

---

# 5. Common Columns

Every business table should include:

```text
id (UUID)

created_at

updated_at

deleted_at
```

Business-owned tables should also include:

```text
business_id
```

---

# 6. Core Tables

Nimbus MVP includes the following tables:

1. users
2. businesses
3. stores
4. categories
5. suppliers
6. products
7. inventory
8. sales
9. forecasts
10. notifications
11. settings
12. csv_uploads
13. ai_conversations
14. analytics_snapshots
15. audit_logs

---

# 7. users

Purpose

Stores authenticated platform users.

Columns

* id
* business_id
* first_name
* last_name
* email
* password_hash
* role
* phone
* is_active
* last_login
* created_at
* updated_at
* deleted_at

Relationships

Business

↓

Many Users

---

# 8. businesses

Purpose

Represents one retail organization.

Columns

* id
* name
* industry
* logo_url
* currency
* timezone
* country
* address
* contact_email
* contact_phone
* subscription_plan
* created_at
* updated_at

Relationships

Business

↓

Stores

Users

Products

Inventory

Sales

Forecasts

Notifications

---

# 9. stores

Purpose

Supports multiple physical store locations.

Columns

* id
* business_id
* name
* address
* city
* state
* postal_code
* country
* latitude
* longitude
* created_at
* updated_at

One Business

↓

Many Stores

---

# 10. categories

Purpose

Groups products.

Examples

Beverages

Electronics

Medicines

Stationery

Relationships

Category

↓

Many Products

---

# 11. suppliers

Purpose

Stores supplier information.

Columns

* id
* business_id
* company_name
* contact_name
* email
* phone
* address
* lead_time_days
* notes
* created_at
* updated_at

---

# 12. products

Purpose

Stores every sellable item.

Columns

* id
* business_id
* category_id
* supplier_id
* sku
* barcode
* name
* description
* selling_price
* cost_price
* unit
* minimum_stock
* maximum_stock
* reorder_point
* safety_stock
* image_url
* created_at
* updated_at

Relationships

Product

↓

Inventory

Sales

Forecasts

---

# 13. inventory

Purpose

Current stock.

Columns

* id
* product_id
* store_id
* quantity
* reserved_quantity
* damaged_quantity
* available_quantity
* last_stock_update
* created_at
* updated_at

One Product

↓

One Inventory Record per Store

---

# 14. sales

Purpose

Historical sales data.

This is the most important table for ML.

Columns

* id
* business_id
* product_id
* store_id
* sale_date
* quantity
* unit_price
* total_amount
* discount
* created_at

Indexes should exist on:

* product_id
* sale_date
* store_id

---

# 15. forecasts

Purpose

Stores generated predictions.

Columns

* id
* product_id
* forecast_date
* predicted_demand
* confidence_score
* reorder_point
* safety_stock
* recommended_quantity
* generated_at

Historical forecasts should never be overwritten.

---

# 16. csv_uploads

Purpose

Tracks uploaded CSV files.

Columns

* id
* business_id
* uploaded_by
* file_name
* upload_status
* records_processed
* records_failed
* uploaded_at

---

# 17. notifications

Purpose

Stores alerts.

Types

Low Stock

Overstock

Forecast Complete

CSV Failed

Inventory Warning

Columns

* id
* business_id
* user_id
* title
* message
* type
* is_read
* created_at

---

# 18. settings

Purpose

Business preferences.

Stores

Notification Settings

Theme

AI Preferences

Forecast Preferences

Currency

Timezone

---

# 19. ai_conversations

Purpose

Stores AI Chat history.

Columns

* id
* business_id
* user_id
* conversation_id
* role
* message
* timestamp

---

# 20. analytics_snapshots

Purpose

Stores calculated KPIs.

Examples

Revenue

Forecast Accuracy

Inventory Value

Inventory Turnover

Profit Margin

Demand Trend

Rather than recalculating expensive metrics every request, snapshots can be refreshed periodically.

---

# 21. audit_logs

Purpose

Tracks important actions.

Examples

Login

CSV Upload

Forecast Generated

Inventory Updated

Settings Changed

Columns

* id
* user_id
* action
* entity
* entity_id
* ip_address
* created_at

---

# 22. Relationships

```text
Business
│
├── Users
├── Stores
├── Products
├── Suppliers
├── Categories
├── Inventory
├── Sales
├── Forecasts
├── Notifications
├── CSV Uploads
└── AI Conversations

Category
│
└── Products

Supplier
│
└── Products

Product
│
├── Inventory
├── Sales
└── Forecasts

User
│
├── Notifications
├── AI Conversations
└── Audit Logs
```

---

# 23. Indexing Strategy

Create indexes on:

* email
* sku
* barcode
* sale_date
* product_id
* business_id
* store_id
* category_id
* supplier_id
* forecast_date

Composite indexes:

* (business_id, product_id)
* (business_id, sale_date)
* (product_id, sale_date)

---

# 24. Soft Deletes

Business data should never be permanently deleted.

Instead:

```text
deleted_at TIMESTAMP NULL
```

Deleted records remain recoverable.

---

# 25. UUID Strategy

Every primary key:

UUID v4

Never use auto-increment integers.

---

# 26. Foreign Keys

Use cascading deletes sparingly.

Recommended:

Business

↓

Restrict Delete

Product

↓

Restrict Delete

Inventory

↓

Cascade on Product removal only if the product itself is intentionally deleted after business confirmation.

---

# 27. Future Tables

Not part of MVP but planned.

* purchase_orders
* invoices
* shipments
* barcode_scans
* stock_movements
* customer_segments
* pricing_rules
* demand_events
* integrations
* scheduled_jobs

---

# 28. Backup Strategy

Supabase automated backups.

Daily snapshots.

Point-in-time recovery when available.

---

# 29. Migration Strategy

Every schema change must be:

* Created with Alembic
* Reviewed
* Version controlled
* Tested before deployment

No manual production edits.

---

# 30. Performance Goals

The database should comfortably support:

* 100+ businesses
* Millions of sales records
* Thousands of products per business
* Concurrent dashboard usage
* Fast forecast retrieval

Scaling should primarily involve indexing, query optimization, and read-heavy analytics strategies before considering architectural changes.

---

# 31. Database Principles

* Every table has a clear responsibility.
* Every relationship is explicit.
* Historical data is preserved whenever practical.
* Business isolation is mandatory.
* Security and consistency take precedence over convenience.
* The schema should evolve through migrations, never through ad-hoc changes.
