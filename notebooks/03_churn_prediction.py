import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

print('='*80)
print('CHURN PREDICTION MODEL - RANDOM FOREST CLASSIFIER')
print('='*80)

# Load data
print('\n[1] Loading Data & Feature Engineering...')
sales_df = pd.read_csv('../data/sales_data.csv')
customer_df = pd.read_csv('../data/customer_info.csv')

sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
reference_date = sales_df['order_date'].max()

# Define Churn: No purchase in last 90 days
churn_threshold_days = 90

# Create churn label
recency = sales_df.groupby('customer_id')['order_date'].max()
recency_days = (reference_date - recency).dt.days

churn_label = (recency_days > churn_threshold_days).astype(int)
churn_df = pd.DataFrame({
    'customer_id': recency.index,
    'churned': churn_label.values
})

print(f'\nChurn Definition: No purchase in last {churn_threshold_days} days')
print(f'Total Customers: {len(churn_df)}')
print(f'Churned: {churn_label.sum()} ({churn_label.sum()/len(churn_df)*100:.1f}%)')
print(f'Active: {(1-churn_label).sum()} ({(1-churn_label).sum()/len(churn_df)*100:.1f}%)')

# Feature Engineering
print('\n[2] FEATURE ENGINEERING')

features = sales_df.groupby('customer_id').agg({
    'order_date': ['min', 'max', 'count'],
    'purchase_amount': ['sum', 'mean', 'std', 'min', 'max'],
    'quantity': ['sum', 'mean'],
    'discount_applied': 'mean',
    'return_status': lambda x: (x == 'Yes').sum(),
    'product_category': 'nunique',
    'region': 'nunique',
    'payment_method': 'nunique'
})

features.columns = ['first_purchase_date', 'last_purchase_date', 'total_transactions',
                   'total_spent', 'avg_order_value', 'order_value_std', 'min_order_value', 'max_order_value',
                   'total_quantity', 'avg_quantity', 'avg_discount', 'return_count',
                   'unique_categories', 'unique_regions', 'unique_payment_methods']

features = features.reset_index()

# Calculate additional features
features['customer_tenure_days'] = (features['last_purchase_date'] - features['first_purchase_date']).dt.days
features['recency_days'] = (reference_date - features['last_purchase_date']).dt.days
features['days_since_first_purchase'] = (reference_date - features['first_purchase_date']).dt.days
features['repeat_rate'] = features['total_transactions'] / (features['days_since_first_purchase'] + 1)
features['return_rate'] = features['return_count'] / features['total_transactions']
features['avg_discount'] = features['avg_discount'].fillna(0)

# Handle NaN values
features['order_value_std'] = features['order_value_std'].fillna(0)

print('\nFeatures Created:')
print(features.columns.tolist())
print(f'\nFeature Summary:')
print(features[['total_spent', 'total_transactions', 'customer_tenure_days', 'recency_days']].describe())

# Merge with churn label
model_data = features.merge(churn_df, on='customer_id')

print(f'\nModel Data Shape: {model_data.shape}')

# Select features for modeling
feature_cols = ['total_transactions', 'total_spent', 'avg_order_value',
                'avg_discount', 'return_rate', 'unique_categories',
                'unique_regions', 'customer_tenure_days', 'recency_days',
                'repeat_rate', 'order_value_std']

X = model_data[feature_cols].copy()
y = model_data['churned'].copy()

print(f'\nX shape: {X.shape}')
print(f'y distribution:\n{y.value_counts()}')

# Train-Test Split
print('\n[3] MODEL TRAINING')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f'Training set: {X_train.shape[0]} samples')
print(f'Test set: {X_test.shape[0]} samples')

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf_model.fit(X_train_scaled, y_train)

print('\nRandom Forest Model Trained')
print(f'Model Parameters: n_estimators=100, max_depth=10')

# Predictions
print('\n[4] MODEL EVALUATION')
y_pred = rf_model.predict(X_test_scaled)
y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]

print('\nClassification Report:')
print(classification_report(y_test, y_pred, target_names=['Active', 'Churned']))

print('\nConfusion Matrix:')
print(confusion_matrix(y_test, y_pred))

roc_auc = roc_auc_score(y_test, y_pred_proba)
print(f'\nROC-AUC Score: {roc_auc:.4f}')

# Feature Importance
print('\n[5] FEATURE IMPORTANCE')
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print('\nTop 10 Most Important Features:')
print(feature_importance.head(10).to_string(index=False))

print('\nFeature Importance Interpretation:')
for idx, row in feature_importance.head(5).iterrows():
    print(f'{idx+1}. {row["feature"]}: {row["importance"]:.4f}')

# High-Risk Customers
print('\n[6] HIGH-RISK CUSTOMERS (Churn Probability > 60%)')
model_data['churn_probability'] = rf_model.predict_proba(scaler.transform(X))[:, 1]
high_risk = model_data[model_data['churn_probability'] > 0.6].sort_values('churn_probability', ascending=False)

print(f'\nHigh-Risk Customers: {len(high_risk)} ({len(high_risk)/len(model_data)*100:.1f}%)')
print('\nTop 10 High-Risk Customers:')
print(high_risk[['customer_id', 'total_spent', 'total_transactions', 'recency_days', 'churn_probability']].head(10).to_string(index=False))

# Revenue at Risk
revenue_at_risk = high_risk['total_spent'].sum()
print(f'\nTotal Revenue at Risk (Churn Probability > 60%): Rp {revenue_at_risk:,.0f}')

print('\n' + '='*80)
print('CHURN PREDICTION COMPLETE')
print('='*80)

print('\nRETENTION STRATEGY BY RISK LEVEL:')
print('\n1. CRITICAL RISK (Churn Probability > 80%)')
print('   - Immediate intervention required')
print('   - Personal outreach from account manager')
print('   - Special retention offer (discount, exclusive access)')
print('   - Expected Impact: 30-40% recovery rate')

print('\n2. HIGH RISK (Churn Probability 60-80%)')
print('   - Proactive engagement campaign')
print('   - Email/SMS personalized communication')
print('   - Product recommendations based on history')
print('   - Expected Impact: 40-50% recovery rate')

print('\n3. MEDIUM RISK (Churn Probability 40-60%)')
print('   - Nurture campaign with value-added content')
print('   - Loyalty program incentives')
print('   - Regular check-in communications')
print('   - Expected Impact: 50-60% recovery rate')

print('\n4. LOW RISK (Churn Probability < 40%)')
print('   - Standard retention through loyalty programs')
print('   - Regular promotional campaigns')
print('   - Community engagement')
print('   - Expected Impact: 60-70% retention rate')
