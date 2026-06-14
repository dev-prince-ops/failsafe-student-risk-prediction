# FAILSAFE

AI-powered Student Risk Prediction and Intervention System

## Overview

FAILSAFE predicts students at risk of academic failure using machine learning and provides explainable recommendations for intervention.

The system combines:

* XGBoost risk prediction
* SHAP explainability
* Intervention recommendation engine
* FastAPI backend
* PostgreSQL database
* React dashboard

## Features

### Authentication

* Teacher registration
* Teacher login
* JWT authentication

### Risk Prediction

* Single student prediction
* Bulk CSV upload
* Risk score generation
* Risk level classification

### Explainability

* SHAP feature importance
* Student-level explanations
* Interactive visualizations

### Intervention Engine

* Automatic intervention generation
* Intervention tracking
* Completion status monitoring

### Dashboard

* Student management
* Risk distribution pie chart
* Student detail pages
* Database persistence

## Technology Stack

### Frontend

* React
* Axios
* React Router
* Recharts

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL

### Machine Learning

* XGBoost
* SHAP
* Scikit-Learn

## Model Performance

Accuracy  : 0.7089
Precision : 0.5517
Recall    : 0.6154
F1 Score  : 0.5818
ROC AUC   : 0.7104

## Future Improvements

* Email alerts
* Advanced intervention tracking
* Improved model tuning
* Responsive mobile interface
* Multi-role access control
