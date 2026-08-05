# Machine Learning Pipeline

**Project:** Nimbus

**Version:** 1.0.0

**Status:** Production Design

---

# 1. Purpose

This document defines the complete Machine Learning architecture used by Nimbus.

It explains:

* Data flow
* Data preprocessing
* Feature engineering
* Model training
* Model evaluation
* Model versioning
* Model deployment
* Prediction pipeline
* Inventory optimization
* Forecast generation
* Future ML improvements

This document acts as the implementation blueprint for every module inside the `/ml` directory.

---

# 2. Goals

Nimbus uses Machine Learning to help retailers:

* Predict future product demand
* Reduce stock-outs
* Reduce overstocking
* Improve purchasing decisions
* Increase inventory turnover
* Improve profitability

The ML system must produce accurate, explainable, and actionable forecasts.

---

# 3. ML Architecture

```text
Historical Sales
        │
        ▼
 CSV Validation
        │
        ▼
 Data Cleaning
        │
        ▼
 Feature Engineering
        │
        ▼
 Dataset Creation
        │
        ▼
 Model Training
        │
        ▼
 Model Evaluation
        │
        ▼
 Model Registry
        │
        ▼
 Saved Model
        │
        ▼
 Prediction API
        │
        ▼
 Inventory Optimization
        │
        ▼
 Dashboard
```

---

# 4. ML Folder Structure

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

utils/

config/

tests/
```

---

# 5. Dataset Sources

Nimbus initially supports:

* CSV Uploads
* Historical Sales
* Inventory Records
* Product Information

Future versions:

* ERP Integrations
* POS Systems
* IoT Inventory Sensors
* Supplier APIs

---

# 6. Required Sales Dataset

Minimum columns:

* Product ID
* Date
* Quantity Sold

Recommended columns:

* Store ID
* Category
* Selling Price
* Discount
* Promotion Flag
* Holiday Flag
* Weather (future)
* Region
* Supplier

---

# 7. Data Validation

Before training, every dataset must be validated.

Checks include:

* Required columns
* Duplicate rows
* Invalid dates
* Missing product IDs
* Negative quantities
* Invalid prices
* Invalid timestamps
* Corrupted CSV files

If validation fails, the upload is rejected with a detailed error report.

---

# 8. Data Cleaning

Cleaning steps:

* Remove duplicate records
* Handle missing values
* Normalize column names
* Standardize date formats
* Remove impossible values
* Convert data types
* Detect extreme outliers (flag for review rather than silently removing)

A preprocessing report should be generated for every upload.

---

# 9. Feature Engineering

The forecasting model should derive features such as:

### Calendar Features

* Day of week
* Week number
* Month
* Quarter
* Year
* Weekend indicator
* Holiday indicator

### Sales Features

* Previous day sales
* Previous week sales
* Previous month sales
* Rolling averages (7, 14, 30 days)
* Rolling standard deviation
* Sales growth rate

### Inventory Features

* Current stock
* Safety stock
* Reorder point

### Product Features

* Category
* Price
* Cost
* Supplier lead time

### Business Features

* Store
* Region
* Currency (future)
* Promotion status

---

# 10. Data Splitting

Recommended split:

* 70% Training
* 15% Validation
* 15% Testing

Time-series data must always preserve chronological order.

Never randomly shuffle historical sales data.

---

# 11. Forecasting Models

Nimbus supports multiple forecasting models.

### Baseline

* Naive Forecast

### Statistical

* Moving Average
* Exponential Smoothing

### Machine Learning

* XGBoost Regressor
* LightGBM Regressor
* Random Forest Regressor

### Time-Series

* Prophet
* SARIMA

### Deep Learning (Future)

* LSTM
* Temporal Fusion Transformer (TFT)
* N-BEATS

For the MVP, the primary model should be **XGBoost**, with Prophet available as an optional benchmark for comparison.

---

# 12. Model Selection Strategy

Train multiple candidate models.

Evaluate each model using the same validation dataset.

Select the best-performing model based on predefined metrics.

Persist the chosen model for inference.

---

# 13. Model Evaluation

Primary Metrics:

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* MAPE (Mean Absolute Percentage Error)

Secondary Metrics:

* R² Score
* Forecast Bias

Evaluation reports should be stored for every trained model.

---

# 14. Model Registry

Every trained model should include metadata:

* Model ID
* Model Type
* Training Date
* Dataset Version
* Feature Set Version
* Hyperparameters
* Evaluation Metrics
* Model Version

Saved models should be immutable.

---

# 15. Model Versioning

Example:

```text
forecast_model_v1.pkl
forecast_model_v2.pkl
forecast_model_v3.pkl
```

Older models should remain available for rollback and comparison.

---

# 16. Prediction Pipeline

```text
User Requests Forecast
        │
        ▼
Backend Calls ML Service
        │
        ▼
Load Latest Approved Model
        │
        ▼
Load Feature Data
        │
        ▼
Generate Predictions
        │
        ▼
Calculate Confidence
        │
        ▼
Run Inventory Optimization
        │
        ▼
Save Forecast
        │
        ▼
Return API Response
```

---

# 17. Confidence Score

Each forecast should include a confidence score.

The score should consider:

* Historical model performance
* Prediction variance
* Data completeness
* Amount of historical data available

Display the confidence score in the dashboard to help users judge forecast reliability.

---

# 18. Inventory Optimization

The optimization engine runs after demand forecasting.

Inputs:

* Forecasted demand
* Current stock
* Safety stock
* Supplier lead time
* Reorder point
* Minimum stock
* Maximum stock

Outputs:

* Recommended order quantity
* Reorder recommendation
* Overstock warning
* Understock warning
* Stock health score

---

# 19. Safety Stock Calculation

The system should calculate safety stock using configurable business rules.

Inputs may include:

* Average demand
* Demand variability
* Lead time
* Desired service level

The implementation should allow future replacement with more advanced statistical methods without changing the API.

---

# 20. Reorder Point

Reorder point should consider:

* Forecasted demand during lead time
* Safety stock
* Supplier lead time

The calculation should be transparent and explainable to the user.

---

# 21. Forecast Horizons

Supported horizons:

* 7 days
* 14 days
* 30 days
* 60 days
* 90 days

Default horizon:

30 days

---

# 22. Retraining Strategy

The MVP should support manual retraining initiated by an administrator.

Future releases may support scheduled retraining (e.g., weekly or monthly).

Each retraining session must create a new model version rather than overwriting an existing one.

---

# 23. Explainability

Nimbus should provide explanations alongside forecasts.

Examples:

* Demand is increasing compared to the previous month.
* Seasonal demand is expected during the upcoming holiday period.
* Current stock is insufficient to meet projected demand.

The goal is to help users understand recommendations rather than treating the model as a black box.

---

# 24. AI Assistant Integration

The AI assistant does **not** generate forecasts.

Instead, it interprets ML outputs and explains them in natural language.

Examples:

* Summarize forecast trends.
* Explain low-confidence predictions.
* Recommend inventory actions.
* Answer business questions using available analytics.

---

# 25. Backend Integration

The FastAPI backend communicates with the ML layer through dedicated service interfaces.

Typical flow:

```text
Forecast API
        │
        ▼
Forecast Service
        │
        ▼
ML Inference Module
        │
        ▼
Prediction
        │
        ▼
Inventory Optimizer
        │
        ▼
Database
```

This separation keeps ML logic independent from API logic.

---

# 26. Performance Targets

Forecast generation should:

* Load the production model efficiently.
* Handle thousands of products without excessive memory usage.
* Return forecasts within an acceptable user-facing response time for the MVP.
* Scale through batching or background jobs as dataset sizes increase.

---

# 27. Monitoring

Track:

* Number of forecasts generated
* Model inference time
* Forecast accuracy
* Prediction failures
* Data validation failures
* Model version usage

Logs should support debugging without exposing sensitive business data.

---

# 28. Future Enhancements

Planned improvements include:

* Automatic model selection
* Hyperparameter optimization
* Ensemble forecasting
* Probabilistic forecasts
* Promotion-aware forecasting
* Weather-aware forecasting
* Holiday-aware forecasting
* Multi-store forecasting
* Product similarity modeling
* Supplier risk prediction
* Demand anomaly detection
* Dynamic pricing recommendations

---

# 29. ML Principles

The ML system should always prioritize:

* Accuracy
* Explainability
* Reproducibility
* Maintainability
* Scalability
* Business value

Complex models should only be adopted when they deliver measurable improvements over simpler alternatives.

---

# 30. Definition of Done

A forecasting pipeline is considered production-ready when it:

* Successfully validates uploaded datasets.
* Produces reproducible forecasts.
* Stores versioned models.
* Returns confidence scores.
* Generates inventory recommendations.
* Integrates cleanly with the FastAPI backend.
* Persists forecast results to the database.
* Provides user-friendly explanations through the AI assistant.
* Is fully documented and testable.
