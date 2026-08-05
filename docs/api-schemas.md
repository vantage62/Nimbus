# API Schemas

**Project:** Nimbus

**Version:** 1.0.0

**Part:** 1 — Core Models, Authentication, Users & Business

---

# 1. Purpose

This document defines all API request and response schemas used by Nimbus.

The schemas are designed for:

* FastAPI + Pydantic v2
* OpenAPI 3.1
* TypeScript type generation
* Frontend/backend contract validation
* Long-term API stability

---

# 2. API Standards

### Base URL

```text
/api/v1
```

---

### Content-Type

```http
application/json
```

---

### UUID Format

Every primary key is represented as:

```json
"550e8400-e29b-41d4-a716-446655440000"
```

---

### Timestamp Format

ISO-8601 UTC

```json
2026-08-04T15:30:00Z
```

---

# 3. Standard Response Envelope

Every successful response follows:

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

### Schema

```python
class ApiResponse:
    success: bool
    message: str
    data: Any
```

---

# 4. Pagination Response

```json
{
    "success": true,
    "data": [],
    "pagination": {
        "page": 1,
        "page_size": 20,
        "total_items": 120,
        "total_pages": 6,
        "has_next": true,
        "has_previous": false
    }
}
```

---

### Pagination Schema

```python
class Pagination:
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
```

---

# 5. Error Response

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Email is invalid.",
        "details": {}
    }
}
```

---

### Error Schema

```python
class ApiError:
    code: str
    message: str
    details: dict | None
```

---

# 6. Validation Error

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Validation failed.",
        "fields": {
            "email": [
                "Invalid email address"
            ]
        }
    }
}
```

---

# 7. Authentication Schemas

## Register Request

```python
class RegisterRequest:

    business_name: str

    first_name: str
    last_name: str

    email: EmailStr
    password: str

    phone: str | None
```

---

## Register Response

```python
class RegisterResponse:

    user_id: UUID
    business_id: UUID

    access_token: str
    refresh_token: str

    expires_in: int
```

---

## Login Request

```python
class LoginRequest:

    email: EmailStr

    password: str
```

---

## Login Response

```python
class LoginResponse:

    access_token: str

    refresh_token: str

    token_type: str

    expires_in: int

    user: UserSummary
```

---

## Refresh Token Request

```python
class RefreshTokenRequest:

    refresh_token: str
```

---

## Refresh Token Response

```python
class RefreshTokenResponse:

    access_token: str

    expires_in: int
```

---

## Logout Request

```python
class LogoutRequest:

    refresh_token: str
```

---

## Password Change

```python
class ChangePasswordRequest:

    current_password: str

    new_password: str
```

---

## Password Reset Request

```python
class ForgotPasswordRequest:

    email: EmailStr
```

---

## Password Reset

```python
class ResetPasswordRequest:

    token: str

    new_password: str
```

---

# 8. User Schemas

## User Summary

```python
class UserSummary:

    id: UUID

    first_name: str

    last_name: str

    email: EmailStr

    role: str
```

---

## User Detail

```python
class UserDetail:

    id: UUID

    business_id: UUID

    first_name: str

    last_name: str

    email: EmailStr

    phone: str | None

    role: str

    is_active: bool

    created_at: datetime

    updated_at: datetime
```

---

## Create User

```python
class CreateUserRequest:

    first_name: str

    last_name: str

    email: EmailStr

    phone: str | None

    role_id: UUID

    password: str
```

---

## Update User

```python
class UpdateUserRequest:

    first_name: str | None

    last_name: str | None

    phone: str | None

    role_id: UUID | None

    is_active: bool | None
```

---

# 9. Business Schemas

## Business Summary

```python
class BusinessSummary:

    id: UUID

    name: str

    industry: str

    currency: str

    timezone: str
```

---

## Business Detail

```python
class BusinessDetail:

    id: UUID

    name: str

    industry: str

    description: str | None

    email: EmailStr | None

    phone: str | None

    website: HttpUrl | None

    address: str | None

    city: str | None

    state: str | None

    country: str

    postal_code: str | None

    currency: str

    timezone: str

    logo_url: str | None

    created_at: datetime

    updated_at: datetime
```

---

## Update Business

```python
class UpdateBusinessRequest:

    name: str | None

    description: str | None

    email: EmailStr | None

    phone: str | None

    website: HttpUrl | None

    address: str | None

    city: str | None

    state: str | None

    country: str | None

    postal_code: str | None

    currency: str | None

    timezone: str | None
```

---

# 10. Shared Enums

## Job Status

```python
class JobStatus(str, Enum):

    QUEUED

    RUNNING

    COMPLETED

    FAILED
```

---

## User Status

```python
class UserStatus(str, Enum):

    ACTIVE

    INACTIVE

    SUSPENDED
```

---

## Notification Type

```python
class NotificationType(str, Enum):

    INFO

    SUCCESS

    WARNING

    ERROR
```

---

## Forecast Status

```python
class ForecastStatus(str, Enum):

    PENDING

    TRAINING

    READY

    FAILED
```

---

# 11. HTTP Status Code Convention

| Status | Meaning               |
| ------ | --------------------- |
| 200    | Success               |
| 201    | Resource Created      |
| 204    | No Content            |
| 400    | Bad Request           |
| 401    | Unauthorized          |
| 403    | Forbidden             |
| 404    | Resource Not Found    |
| 409    | Conflict              |
| 422    | Validation Error      |
| 429    | Too Many Requests     |
| 500    | Internal Server Error |

---

# 12. Naming Rules

All API schemas should:

* Use PascalCase for model names.
* Use snake_case for JSON fields where the backend expects them.
* Use UUIDs for identifiers.
* Use ISO-8601 timestamps.
* Be backwards compatible whenever possible.

---

# 13. Versioning Policy

Breaking changes must result in a new API version (for example, `/api/v2`).

Non-breaking additions may be introduced within the current version.

Deprecated fields should remain available for at least one major release before removal.

---

# 14. Definition of Done

This section is complete when:

* Authentication schemas are implemented.
* User schemas are implemented.
* Business schemas are implemented.
* Shared response models are implemented.
* Error handling follows the standard envelope.
* OpenAPI documentation is generated successfully.

# API Schemas

**Project:** Nimbus

**Version:** 1.0.0

**Part:** 2 — Dashboard, Products, Categories, Inventory & Stock Movements

---

# 1. Dashboard Schemas

## Dashboard Summary Response

```python
class DashboardSummary:

    total_products: int

    total_categories: int

    total_inventory_items: int

    inventory_value: Decimal

    low_stock_products: int

    out_of_stock_products: int

    active_forecasts: int

    unread_notifications: int
```

---

## Sales Overview

```python
class SalesOverview:

    today_sales: Decimal

    weekly_sales: Decimal

    monthly_sales: Decimal

    yearly_sales: Decimal
```

---

## Forecast Overview

```python
class ForecastOverview:

    generated_at: datetime

    forecast_accuracy: float

    next_restock_date: date | None

    predicted_stockouts: int

    recommended_reorders: int
```

---

## Dashboard Response

```python
class DashboardResponse:

    summary: DashboardSummary

    sales: SalesOverview

    forecast: ForecastOverview

    notifications: list[NotificationSummary]
```

---

# 2. Category Schemas

## Category

```python
class Category:

    id: UUID

    business_id: UUID

    name: str

    description: str | None

    created_at: datetime

    updated_at: datetime
```

---

## Create Category

```python
class CreateCategoryRequest:

    name: str

    description: str | None
```

---

## Update Category

```python
class UpdateCategoryRequest:

    name: str | None

    description: str | None
```

---

# 3. Product Schemas

## Product Summary

```python
class ProductSummary:

    id: UUID

    sku: str

    name: str

    category_name: str

    current_stock: int

    reorder_level: int

    selling_price: Decimal
```

---

## Product Detail

```python
class ProductDetail:

    id: UUID

    business_id: UUID

    category_id: UUID

    sku: str

    barcode: str | None

    name: str

    description: str | None

    unit: str

    cost_price: Decimal

    selling_price: Decimal

    reorder_level: int

    current_stock: int

    maximum_stock: int | None

    image_url: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime
```

---

## Create Product

```python
class CreateProductRequest:

    category_id: UUID

    sku: str

    barcode: str | None

    name: str

    description: str | None

    unit: str

    cost_price: Decimal

    selling_price: Decimal

    reorder_level: int

    maximum_stock: int | None
```

---

## Update Product

```python
class UpdateProductRequest:

    category_id: UUID | None

    barcode: str | None

    name: str | None

    description: str | None

    unit: str | None

    cost_price: Decimal | None

    selling_price: Decimal | None

    reorder_level: int | None

    maximum_stock: int | None

    is_active: bool | None
```

---

# 4. Inventory Schemas

## Inventory Item

```python
class InventoryItem:

    id: UUID

    product_id: UUID

    business_id: UUID

    current_stock: int

    reserved_stock: int

    available_stock: int

    reorder_level: int

    maximum_stock: int | None

    inventory_value: Decimal

    last_updated: datetime
```

---

## Inventory Adjustment

```python
class InventoryAdjustmentRequest:

    product_id: UUID

    quantity: int

    reason: str

    notes: str | None
```

---

## Inventory Response

```python
class InventoryResponse:

    product: ProductSummary

    inventory: InventoryItem
```

---

# 5. Stock Movement Schemas

> Although `stock_movements` is planned for a future iteration, the API contracts are defined now to ensure forward compatibility.

## Stock Movement

```python
class StockMovement:

    id: UUID

    product_id: UUID

    business_id: UUID

    movement_type: StockMovementType

    quantity: int

    previous_stock: int

    new_stock: int

    reference: str | None

    notes: str | None

    created_by: UUID

    created_at: datetime
```

---

## Create Stock Movement

```python
class CreateStockMovementRequest:

    product_id: UUID

    movement_type: StockMovementType

    quantity: int

    reference: str | None

    notes: str | None
```

---

# 6. Stock Movement Enum

```python
class StockMovementType(str, Enum):

    SALE = "SALE"

    PURCHASE = "PURCHASE"

    RESTOCK = "RESTOCK"

    RETURN = "RETURN"

    DAMAGE = "DAMAGE"

    ADJUSTMENT = "ADJUSTMENT"

    TRANSFER = "TRANSFER"
```

---

# 7. Search Schemas

## Product Search

```python
class ProductSearchRequest:

    query: str | None

    category_id: UUID | None

    low_stock_only: bool = False

    out_of_stock_only: bool = False

    page: int = 1

    page_size: int = 20
```

---

## Inventory Search

```python
class InventorySearchRequest:

    query: str | None

    category_id: UUID | None

    minimum_stock: int | None

    maximum_stock: int | None

    page: int = 1

    page_size: int = 20
```

---

# 8. Inventory KPI Schemas

```python
class InventoryKPIs:

    total_products: int

    inventory_value: Decimal

    average_stock_level: float

    stock_turnover_ratio: float

    low_stock_items: int

    out_of_stock_items: int

    dead_stock_items: int
```

---

# 9. Bulk Operations

## Bulk Product Import

```python
class BulkProductImportRequest:

    file_id: UUID
```

---

## Bulk Product Delete

```python
class BulkDeleteProductsRequest:

    product_ids: list[UUID]
```

---

## Bulk Inventory Update

```python
class BulkInventoryUpdateRequest:

    updates: list[InventoryAdjustmentRequest]
```

---

# 10. Dashboard Charts

## Inventory Trend

```python
class InventoryTrendPoint:

    date: date

    inventory_value: Decimal
```

---

## Sales Trend

```python
class SalesTrendPoint:

    date: date

    revenue: Decimal
```

---

## Forecast Trend

```python
class ForecastTrendPoint:

    date: date

    predicted_demand: float
```

---

# 11. Validation Rules

### SKU

* Required
* Unique per business
* Maximum 100 characters

### Product Name

* Required
* Maximum 255 characters

### Cost Price

* Must be greater than or equal to 0

### Selling Price

* Must be greater than or equal to Cost Price

### Reorder Level

* Must be greater than or equal to 0

### Stock Quantity

* Cannot become negative through standard operations unless explicitly supported by business rules.

---

# 12. API Conventions

All inventory operations must:

* Respect `business_id` isolation.
* Validate permissions.
* Record audit logs.
* Generate stock movement records when applicable.
* Update inventory atomically within a database transaction.

---

# 13. Definition of Done

This section is complete when:

* Product CRUD schemas are implemented.
* Category CRUD schemas are implemented.
* Inventory schemas are implemented.
* Dashboard response models are implemented.
* Search and pagination contracts are defined.
* Stock movement models are available for future implementation.
* Validation rules are enforced through Pydantic models.

# API Schemas

**Project:** Nimbus

**Version:** 1.0.0

**Part:** 3 — Sales History, CSV Upload, Jobs, Forecasting & Analytics

---

# 1. Sales History Schemas

Sales history is the primary source of truth for demand forecasting.

Every completed sale should create a sales history record.

---

## Sales Record

```python
class SalesRecord:

    id: UUID

    business_id: UUID

    product_id: UUID

    quantity_sold: int

    unit_price: Decimal

    discount: Decimal

    total_amount: Decimal

    sales_channel: str

    sale_timestamp: datetime

    created_at: datetime
```

---

## Create Sales Record

```python
class CreateSalesRecordRequest:

    product_id: UUID

    quantity_sold: int

    unit_price: Decimal

    discount: Decimal = 0

    sales_channel: str

    sale_timestamp: datetime
```

---

## Sales Summary

```python
class SalesSummary:

    total_sales: Decimal

    total_units_sold: int

    average_order_value: Decimal

    best_selling_product: str

    period_start: datetime

    period_end: datetime
```

---

# 2. CSV Upload Schemas

Nimbus supports importing historical data through CSV files.

---

## Upload CSV Request

```python
class UploadCSVRequest:

    file: UploadFile

    dataset_type: DatasetType
```

---

## Upload CSV Response

```python
class UploadCSVResponse:

    upload_id: UUID

    filename: str

    dataset_type: DatasetType

    status: JobStatus

    uploaded_at: datetime
```

---

## CSV Validation Result

```python
class CSVValidationResult:

    total_rows: int

    valid_rows: int

    invalid_rows: int

    warnings: list[str]

    errors: list[str]
```

---

## Dataset Type

```python
class DatasetType(str, Enum):

    SALES = "SALES"

    INVENTORY = "INVENTORY"

    PRODUCTS = "PRODUCTS"
```

---

# 3. Background Job Schemas

Long-running operations are tracked through jobs.

Examples:

* CSV import
* Forecast generation
* Model training
* Analytics refresh

---

## Job

```python
class Job:

    id: UUID

    business_id: UUID

    job_type: JobType

    status: JobStatus

    progress: int

    created_at: datetime

    started_at: datetime | None

    completed_at: datetime | None

    error_message: str | None
```

---

## Job Type

```python
class JobType(str, Enum):

    CSV_IMPORT

    FORECAST

    MODEL_TRAINING

    ANALYTICS_REFRESH

    EXPORT
```

---

# 4. Forecast Schemas

---

## Forecast Request

```python
class ForecastRequest:

    product_ids: list[UUID] | None

    forecast_days: int

    include_confidence_interval: bool = True
```

---

## Product Forecast

```python
class ProductForecast:

    product_id: UUID

    predicted_demand: float

    confidence_score: float

    recommended_stock: int

    reorder_quantity: int

    expected_stockout_date: date | None
```

---

## Forecast Response

```python
class ForecastResponse:

    forecast_id: UUID

    generated_at: datetime

    model_version: str

    products: list[ProductForecast]
```

---

## Forecast Metrics

```python
class ForecastMetrics:

    mae: float

    rmse: float

    mape: float

    r2_score: float
```

---

# 5. Model Registry Schemas

---

## Model Information

```python
class ModelInfo:

    id: UUID

    version: str

    algorithm: str

    trained_at: datetime

    dataset_size: int

    status: str

    mae: float

    rmse: float

    mape: float
```

---

# 6. Inventory Optimization

---

## Recommendation

```python
class InventoryRecommendation:

    product_id: UUID

    current_stock: int

    predicted_demand: int

    recommended_stock: int

    reorder_quantity: int

    priority: str

    explanation: str
```

---

## Optimization Response

```python
class InventoryOptimizationResponse:

    recommendations: list[InventoryRecommendation]

    generated_at: datetime
```

---

# 7. Analytics Schemas

---

## Analytics Summary

```python
class AnalyticsSummary:

    revenue: Decimal

    inventory_value: Decimal

    inventory_turnover: float

    stockout_rate: float

    forecast_accuracy: float
```

---

## Product Performance

```python
class ProductPerformance:

    product_id: UUID

    product_name: str

    revenue: Decimal

    units_sold: int

    profit: Decimal

    inventory_turnover: float
```

---

## Category Analytics

```python
class CategoryAnalytics:

    category_name: str

    revenue: Decimal

    products: int

    inventory_value: Decimal
```

---

## Forecast Accuracy Trend

```python
class ForecastAccuracyPoint:

    date: date

    accuracy: float
```

---

# 8. Report Export

---

## Export Request

```python
class ExportReportRequest:

    report_type: str

    format: str

    start_date: date

    end_date: date
```

---

## Export Response

```python
class ExportReportResponse:

    job_id: UUID

    status: JobStatus
```

---

# 9. Validation Rules

### Forecast Days

* Minimum: 1
* Maximum: 365

### Quantity Sold

* Must be greater than 0

### Progress

* 0–100

### Confidence Score

* 0.0–1.0

### Accuracy Metrics

* Must be non-negative

---

# 10. Engineering Rules

Forecast generation must:

* Use the active production model.
* Execute asynchronously for large datasets.
* Log every prediction request.
* Record model version.
* Store evaluation metrics.

CSV imports must:

* Validate every row.
* Reject malformed files.
* Produce an import report.
* Run inside database transactions where appropriate.

---

# 11. Definition of Done

This section is complete when:

* Sales history schemas are implemented.
* CSV upload schemas are implemented.
* Background job schemas are implemented.
* Forecast models are implemented.
* Model registry schemas are available.
* Inventory optimization contracts are defined.
* Analytics response models are complete.
* Export contracts are documented.

# API Schemas

**Project:** Nimbus

**Version:** 1.0.0

**Part:** 4 — AI Chat, Voice, Notifications, Settings, Health Checks & System Configuration

---

# 1. AI Chat Schemas

Nimbus includes an AI-powered business assistant capable of answering questions about inventory, forecasting, analytics, and business performance.

The AI must only access data belonging to the authenticated business.

---

## Chat Request

```python
class ChatRequest:

    message: str

    conversation_id: UUID | None

    include_business_context: bool = True
```

---

## Chat Message

```python
class ChatMessage:

    id: UUID

    role: Literal["user", "assistant", "system"]

    content: str

    created_at: datetime
```

---

## Chat Response

```python
class ChatResponse:

    conversation_id: UUID

    message: ChatMessage

    model: str

    tokens_used: int

    response_time_ms: int
```

---

## Conversation Summary

```python
class ConversationSummary:

    id: UUID

    title: str

    last_message_at: datetime

    message_count: int
```

---

# 2. Voice Assistant Schemas

Voice interactions are converted to text before processing by the AI assistant.

---

## Voice Request

```python
class VoiceRequest:

    audio_file: UploadFile

    language: str = "en"
```

---

## Voice Response

```python
class VoiceResponse:

    transcript: str

    ai_response: str

    audio_url: str | None
```

---

## Speech Configuration

```python
class SpeechConfiguration:

    language: str

    voice: str

    speed: float

    pitch: float
```

---

# 3. Notification Schemas

---

## Notification

```python
class Notification:

    id: UUID

    business_id: UUID

    title: str

    message: str

    type: NotificationType

    is_read: bool

    created_at: datetime
```

---

## Create Notification

```python
class CreateNotificationRequest:

    title: str

    message: str

    type: NotificationType
```

---

## Notification Preferences

```python
class NotificationPreferences:

    email_enabled: bool

    push_enabled: bool

    sms_enabled: bool

    low_stock_alerts: bool

    forecast_alerts: bool

    weekly_reports: bool
```

---

# 4. Business Settings Schemas

---

## Business Settings

```python
class BusinessSettings:

    currency: str

    timezone: str

    date_format: str

    language: str

    theme: str

    fiscal_year_start: date

    default_forecast_days: int
```

---

## Update Business Settings

```python
class UpdateBusinessSettingsRequest:

    currency: str | None

    timezone: str | None

    date_format: str | None

    language: str | None

    theme: str | None

    fiscal_year_start: date | None

    default_forecast_days: int | None
```

---

# 5. User Preferences

---

## User Preferences

```python
class UserPreferences:

    dashboard_layout: str

    default_page_size: int

    dark_mode: bool

    email_notifications: bool

    push_notifications: bool

    language: str
```

---

## Update User Preferences

```python
class UpdateUserPreferencesRequest:

    dashboard_layout: str | None

    default_page_size: int | None

    dark_mode: bool | None

    email_notifications: bool | None

    push_notifications: bool | None

    language: str | None
```

---

# 6. Feature Flags

Feature flags allow gradual rollout of new functionality.

---

## Feature Flag

```python
class FeatureFlag:

    key: str

    enabled: bool

    description: str
```

---

## Feature Flags Response

```python
class FeatureFlagsResponse:

    features: list[FeatureFlag]
```

---

# 7. Health Check Schemas

---

## Health Response

```python
class HealthResponse:

    status: str

    version: str

    timestamp: datetime

    uptime_seconds: int
```

---

## Dependency Health

```python
class DependencyHealth:

    service: str

    status: str

    response_time_ms: int
```

---

## Detailed Health Response

```python
class DetailedHealthResponse:

    application: HealthResponse

    database: DependencyHealth

    storage: DependencyHealth

    ai_provider: DependencyHealth

    ml_engine: DependencyHealth
```

---

# 8. System Information

---

## System Info

```python
class SystemInfo:

    application_version: str

    api_version: str

    environment: str

    build_number: str

    deployed_at: datetime
```

---

# 9. AI Usage

Track AI usage for analytics and future billing.

---

## AI Usage Summary

```python
class AIUsageSummary:

    conversations: int

    total_messages: int

    total_tokens: int

    average_response_time_ms: int
```

---

## AI Usage Record

```python
class AIUsageRecord:

    id: UUID

    model: str

    tokens_used: int

    response_time_ms: int

    created_at: datetime
```

---

# 10. Voice Usage

---

## Voice Usage Summary

```python
class VoiceUsageSummary:

    requests: int

    total_audio_duration_seconds: float

    average_processing_time_ms: int
```

---

# 11. Validation Rules

### Chat Message

* Required
* Maximum 10,000 characters

### Notification Title

* Maximum 150 characters

### Notification Message

* Maximum 2,000 characters

### Forecast Default

* Between 1 and 365 days

### Dashboard Page Size

* Between 10 and 100 items

---

# 12. Engineering Rules

AI chat must:

* Respect business isolation.
* Never expose internal secrets.
* Log model version and token usage.
* Apply rate limits.

Voice requests must:

* Accept supported audio formats only.
* Enforce maximum upload size.
* Validate language codes.

Notifications must:

* Be idempotent where appropriate.
* Record delivery status when external channels are added.

Health endpoints must:

* Be lightweight.
* Avoid expensive database queries.
* Return machine-readable status values.

---

# 13. Definition of Done

This section is complete when:

* AI chat schemas are implemented.
* Voice assistant schemas are implemented.
* Notification models are implemented.
* Business settings and user preferences are available.
* Feature flag contracts are defined.
* Health check endpoints follow the documented schemas.
* AI and voice usage tracking models are implemented.

# API Schemas

**Project:** Nimbus

**Version:** 1.0.0

**Part:** 5 — RBAC, Audit Logs, Login History, API Keys, Webhooks & API Governance

---

# 1. Role-Based Access Control (RBAC)

Nimbus uses permission-based authorization rather than hardcoded role checks.

---

## Role

```python
class Role:

    id: UUID

    business_id: UUID

    name: str

    description: str | None

    is_system_role: bool

    created_at: datetime

    updated_at: datetime
```

---

## Create Role

```python
class CreateRoleRequest:

    name: str

    description: str | None

    permissions: list[str]
```

---

## Update Role

```python
class UpdateRoleRequest:

    name: str | None

    description: str | None

    permissions: list[str] | None
```

---

# 2. Permission Schemas

Permissions follow a resource:action convention.

Examples:

```text
inventory:read
inventory:create
inventory:update
inventory:delete

forecast:generate

analytics:view

business:update

users:invite

settings:update
```

---

## Permission

```python
class Permission:

    key: str

    name: str

    description: str

    category: str
```

---

## User Permissions

```python
class UserPermissions:

    user_id: UUID

    role: str

    permissions: list[str]
```

---

# 3. Audit Logs

Every sensitive operation should create an immutable audit record.

---

## Audit Log

```python
class AuditLog:

    id: UUID

    business_id: UUID

    user_id: UUID

    action: str

    resource: str

    resource_id: UUID | None

    ip_address: str

    user_agent: str

    metadata: dict | None

    created_at: datetime
```

---

## Audit Log Search

```python
class AuditLogSearchRequest:

    user_id: UUID | None

    action: str | None

    resource: str | None

    start_date: date | None

    end_date: date | None

    page: int = 1

    page_size: int = 20
```

---

# 4. Login History

Track successful and failed authentication attempts.

---

## Login Record

```python
class LoginHistory:

    id: UUID

    user_id: UUID

    ip_address: str

    user_agent: str

    success: bool

    failure_reason: str | None

    login_at: datetime
```

---

# 5. Session Information

```python
class ActiveSession:

    id: UUID

    device_name: str

    browser: str

    operating_system: str

    ip_address: str

    last_activity: datetime

    current_session: bool
```

---

# 6. API Keys (Future)

Reserved for third-party integrations.

---

## API Key

```python
class ApiKey:

    id: UUID

    business_id: UUID

    name: str

    prefix: str

    permissions: list[str]

    last_used_at: datetime | None

    expires_at: datetime | None

    created_at: datetime
```

---

## Create API Key

```python
class CreateApiKeyRequest:

    name: str

    permissions: list[str]

    expires_at: datetime | None
```

---

## Create API Key Response

```python
class CreateApiKeyResponse:

    api_key: str

    prefix: str

    expires_at: datetime | None
```

**Important:** The full API key is returned only once at creation.

---

# 7. Webhooks (Future)

Support outbound event notifications.

---

## Webhook

```python
class Webhook:

    id: UUID

    business_id: UUID

    url: HttpUrl

    events: list[str]

    secret: str

    enabled: bool

    created_at: datetime
```

---

## Supported Events

```text
inventory.updated

forecast.completed

forecast.failed

csv.import.completed

csv.import.failed

notification.created

user.created

user.deleted
```

---

# 8. Standard Metadata

Every list endpoint should include:

```python
class ResponseMetadata:

    request_id: UUID

    timestamp: datetime

    api_version: str
```

---

# 9. Standard List Response

```python
class ListResponse[T]:

    success: bool

    data: list[T]

    pagination: Pagination

    meta: ResponseMetadata
```

---

# 10. Error Codes

| Code                  | Description                       |
| --------------------- | --------------------------------- |
| VALIDATION_ERROR      | Invalid request payload           |
| UNAUTHORIZED          | Authentication required           |
| FORBIDDEN             | Permission denied                 |
| NOT_FOUND             | Resource does not exist           |
| CONFLICT              | Duplicate or conflicting resource |
| RATE_LIMITED          | Too many requests                 |
| FILE_TOO_LARGE        | Uploaded file exceeds limit       |
| INVALID_FILE          | Unsupported or malformed file     |
| FORECAST_FAILED       | Forecast generation failed        |
| AI_PROVIDER_ERROR     | External AI provider unavailable  |
| INTERNAL_SERVER_ERROR | Unexpected server error           |

---

# 11. API Versioning

Current version:

```text
/api/v1
```

Rules:

* Breaking changes require `/api/v2`.
* Non-breaking additions may be introduced within the same version.
* Deprecated fields remain supported for at least one major version.

---

# 12. Idempotency

The following operations should support idempotency where practical:

* CSV import
* Forecast generation
* Notification creation
* Report export

Support via:

```http
Idempotency-Key: <uuid>
```

---

# 13. Rate Limit Headers

Recommended response headers:

```http
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
Retry-After
```

---

# 14. Correlation IDs

Every request receives a unique identifier.

Example:

```http
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

This identifier should appear in:

* API responses
* Application logs
* Audit logs
* Error reports

---

# 15. OpenAPI Conventions

Every endpoint should include:

* Summary
* Description
* Tags
* Request model
* Response model
* Example payloads
* Error responses
* Authentication requirements

FastAPI should automatically generate the OpenAPI specification and Swagger UI.

---

# 16. Deprecation Policy

When deprecating an endpoint:

1. Mark as deprecated in OpenAPI.
2. Announce in release notes.
3. Provide replacement endpoint.
4. Maintain compatibility through one major version.
5. Remove only after the documented deprecation period.

---

# 17. Engineering Rules

* Every protected endpoint requires authentication.
* Every mutating endpoint records an audit log.
* Every request includes a correlation ID.
* Every list response uses the standard metadata envelope.
* API contracts are considered stable once released.

---

# 18. Definition of Done

The API contract is complete when:

* RBAC models are implemented.
* Permission models are implemented.
* Audit logging is available.
* Login history is recorded.
* API key contracts are defined.
* Webhook contracts are documented.
* Error codes are standardized.
* OpenAPI documentation is generated successfully.
* Versioning and deprecation policies are documented.
