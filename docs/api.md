# Nimbus API Specification

**Version:** 1.0.0
**Status:** Draft

---

# 1. Overview

Nimbus exposes a versioned REST API for all frontend interactions.

All communication between the frontend, machine learning engine, and external AI services is orchestrated through the backend.

The API follows RESTful principles with consistent request and response structures.

---

# 2. Base URL

Development

```text
http://localhost:8000/api/v1
```

Production

```text
https://api.nimbus-ai.com/api/v1
```

---

# 3. Authentication

Authentication uses JWT.

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

Access Tokens

* Short lived

Refresh Tokens

* Long lived

---

# 4. Standard Response Format

## Success

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

## Error

```json
{
    "success": false,
    "message": "Product not found.",
    "code": "PRODUCT_NOT_FOUND"
}
```

---

# 5. Authentication Module

## Register

POST

```text
/auth/register
```

Creates a new business and its first administrator.

Body

```json
{
  "business_name": "",
  "first_name": "",
  "last_name": "",
  "email": "",
  "password": ""
}
```

Response

```json
{
    "success": true,
    "data": {
        "access_token": "...",
        "refresh_token": "..."
    }
}
```

---

## Login

POST

```text
/auth/login
```

Body

```json
{
    "email":"",
    "password":""
}
```

---

## Refresh Token

POST

```text
/auth/refresh
```

---

## Logout

POST

```text
/auth/logout
```

---

## Current User

GET

```text
/auth/me
```

Returns the authenticated user's profile.

---

# 6. Dashboard Module

## Dashboard Summary

GET

```text
/dashboard
```

Returns

* Total Products
* Inventory Value
* Revenue
* Forecast Accuracy
* Low Stock Count
* Overstock Count
* Active Notifications

---

## Dashboard Charts

GET

```text
/dashboard/charts
```

Returns

* Revenue Trend
* Demand Trend
* Inventory Trend
* Forecast Accuracy
* Product Performance

---

# 7. Business Profile Module

## Get Business

GET

```text
/business
```

---

## Update Business

PUT

```text
/business
```

Update

* Name
* Logo
* Address
* Currency
* Timezone
* Industry

---

# 8. Products Module

## Get Products

GET

```text
/products
```

Supports

* Pagination
* Search
* Category Filter
* Supplier Filter

---

## Get Product

GET

```text
/products/{id}
```

---

## Create Product

POST

```text
/products
```

---

## Update Product

PUT

```text
/products/{id}
```

---

## Delete Product

DELETE

```text
/products/{id}
```

Soft delete only.

---

# 9. Categories Module

GET

```text
/categories
```

POST

```text
/categories
```

PUT

```text
/categories/{id}
```

DELETE

```text
/categories/{id}
```

---

# 10. Suppliers Module

GET

```text
/suppliers
```

POST

```text
/suppliers
```

PUT

```text
/suppliers/{id}
```

DELETE

```text
/suppliers/{id}
```

---

# 11. Inventory Module

## Inventory List

GET

```text
/inventory
```

Supports filters:

* Store
* Category
* Supplier
* Low Stock
* Overstock

---

## Inventory Details

GET

```text
/inventory/{product_id}
```

---

## Update Inventory

PATCH

```text
/inventory/{product_id}
```

Adjust stock.

---

## Stock History

GET

```text
/inventory/{product_id}/history
```

Returns historical inventory movements.

(Currently sourced from inventory events. Future versions should use the `stock_movements` table.)

---

## Low Stock

GET

```text
/inventory/low-stock
```

---

## Overstock

GET

```text
/inventory/overstock
```

---

# 12. Sales Module

## Sales History

GET

```text
/sales
```

Supports

* Date range
* Product
* Category
* Store

---

## Add Sale

POST

```text
/sales
```

---

## Import Sales

POST

```text
/sales/import
```

CSV upload endpoint.

---

# 13. Forecasting Module

## Generate Forecast

POST

```text
/forecast
```

Body

```json
{
  "forecast_days":30
}
```

Returns

* Predicted Demand
* Reorder Point
* Safety Stock
* Recommended Quantity
* Confidence Score

---

## Forecast History

GET

```text
/forecast/history
```

---

## Product Forecast

GET

```text
/forecast/{product_id}
```

---

## Forecast Accuracy

GET

```text
/forecast/accuracy
```

---

# 14. CSV Upload Module

## Upload CSV

POST

```text
/upload/csv
```

Supported Files

* Sales
* Inventory
* Products

Multipart upload.

---

## Upload Status

GET

```text
/upload/{upload_id}
```

---

## Upload History

GET

```text
/upload/history
```

---

# 15. Analytics Module

## Business Analytics

GET

```text
/analytics
```

---

## Revenue Analytics

GET

```text
/analytics/revenue
```

---

## Product Analytics

GET

```text
/analytics/products
```

---

## Inventory Analytics

GET

```text
/analytics/inventory
```

---

## Forecast Analytics

GET

```text
/analytics/forecast
```

---

# 16. Notifications Module

## Notifications

GET

```text
/notifications
```

---

## Mark Read

PATCH

```text
/notifications/{id}
```

---

## Mark All Read

PATCH

```text
/notifications/read-all
```

---

# 17. AI Chat Module

## Chat

POST

```text
/chat
```

Body

```json
{
    "message":"Why is demand increasing?"
}
```

Returns

AI generated explanation.

---

## Conversation History

GET

```text
/chat/history
```

---

## Delete Conversation

DELETE

```text
/chat/{conversation_id}
```

---

# 18. Voice Assistant

## Speech To Text

POST

```text
/voice/transcribe
```

---

## Text To Speech

POST

```text
/voice/speak
```

---

## Voice Chat

POST

```text
/voice/chat
```

---

# 19. Settings Module

GET

```text
/settings
```

PUT

```text
/settings
```

Supports

* Theme
* Notifications
* AI Preferences
* Currency
* Timezone

---

# 20. Search

Universal search.

GET

```text
/search
```

Supports

Products

Suppliers

Inventory

Categories

---

# 21. Health Check

GET

```text
/health
```

Returns

* API Status
* Database Status
* ML Status
* AI Provider Status

---

# 22. Error Codes

Authentication

* INVALID_CREDENTIALS
* TOKEN_EXPIRED
* UNAUTHORIZED

Products

* PRODUCT_NOT_FOUND
* DUPLICATE_SKU

Inventory

* INSUFFICIENT_STOCK
* INVENTORY_NOT_FOUND

Forecasting

* FORECAST_FAILED
* MODEL_NOT_AVAILABLE

CSV

* INVALID_FILE
* INVALID_FORMAT
* PARSE_ERROR

General

* VALIDATION_ERROR
* INTERNAL_SERVER_ERROR

---

# 23. Pagination

All list endpoints support:

```text
?page=1

?page_size=20
```

Response

```json
{
    "page":1,
    "page_size":20,
    "total":0,
    "items":[]
}
```

---

# 24. Filtering

Supported query parameters include:

```text
?search=

?category=

?supplier=

?store=

?start_date=

?end_date=

?sort=

?order=
```

---

# 25. API Versioning

Current version

```text
/api/v1/
```

Future versions

```text
/api/v2/

/api/v3/
```

Older versions remain supported during migration windows.

---

# 26. Rate Limiting

Recommended defaults:

* Auth endpoints: 10 requests/minute
* AI Chat: 30 requests/minute
* Forecast generation: 20 requests/minute
* CSV Upload: 10 requests/hour
* General API: 120 requests/minute

---

# 27. Security

Every protected endpoint requires:

* JWT authentication
* Business isolation (`business_id`)
* Role-based authorization where applicable
* Request validation
* HTTPS in production

---

# 28. OpenAPI Documentation

FastAPI should automatically expose:

```text
/docs
```

Swagger UI

and

```text
/redoc
```

ReDoc documentation.

---

# 29. API Design Principles

Every endpoint must:

* Be RESTful
* Be versioned
* Return consistent response structures
* Validate input using Pydantic
* Return meaningful HTTP status codes
* Include descriptive OpenAPI metadata
* Respect business-level data isolation

---

# 30. Future API Modules

Planned endpoints for future releases:

* Purchase Orders
* Warehouse Transfers
* Barcode Scanning
* ERP Integrations
* POS Integrations
* OCR Invoice Processing
* Scheduled Reports
* Webhooks
* Public API Keys
* Third-Party Integrations

These modules are intentionally excluded from the MVP but should follow the same architectural and response conventions defined in this document.
