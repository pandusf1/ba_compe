import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

print('='*80)
print('CUSTOMER SEGMENTATION ANALYSIS - RFM & K-MEANS CLUSTERING')
print('='*80)

# Load data
print('\n[1] Loading Data...')
sales_df = pd.read_csv('../data/sales_data.csv')
customer_df = pd.read_csv('../data/customer_info.csv')

sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
reference_date = sales_df['order_date'].max()
print(f'Reference Date: {reference_date.date()}')

# RFM Analysis
print('\n[2] RFM (Recency, Frequency, Monetary) CALCULATION')

rfm_data = sales_df.groupby('customer_id').agg({
    'order_date': lambda x: (reference_date - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'purchase_amount': 'sum'  # Monetary
})

rfm_data.columns = ['Recency', 'Frequency', 'Monetary']
rfm_data = rfm_data.reset_index()

print('\nRFM Summary Statistics:')
print(rfm_data[['Recency', 'Frequency', 'Monetary']].describe())

print('\nSample RFM Data (Top 10 by Monetary):')
print(rfm_data.nlargest(10, 'Monetary'))

# RFM Scoring (1-5 scale)
print('\n[3] RFM SCORING (1-5 scale)')
rfm_data['R_Score'] = pd.qcut(rfm_data['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm_data['F_Score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
rfm_data['M_Score'] = pd.qcut(rfm_data['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')

rfm_data['RFM_Score'] = rfm_data['R_Score'].astype(str) + rfm_data['F_Score'].astype(str) + rfm_data['M_Score'].astype(str)

print('\nRFM Score Distribution:')
print(rfm_data['RFM_Score'].value_counts().head(10))

# Manual Segmentation Rules
print('\n[4] CUSTOMER SEGMENTATION - BUSINESS RULES')

def segment_customer(row):
    if (row['R_Score'] >= 4) and (row['F_Score'] >= 4) and (row['M_Score'] >= 4):
        return 'Champions'
    elif (row['R_Score'] >= 4) and (row['F_Score'] >= 3):
        return 'Loyal Customers'
    elif (row['R_Score'] >= 3) and (row['M_Score'] >= 4):
        return 'Big Spenders'
    elif (row['R_Score'] >= 4):
        return 'Recent Customers'
    elif (row['F_Score'] >= 4) and (row['M_Score'] >= 4):
        return 'VIP/Core'
    elif (row['R_Score'] <= 2) and (row['F_Score'] >= 3):
        return 'At Risk'
    elif (row['R_Score'] <= 2):
        return 'Lost Customers'
    else:
        return 'Potential'

rfm_data['Segment'] = rfm_data.apply(segment_customer, axis=1)

print('\nSegment Distribution:')
segment_dist = rfm_data['Segment'].value_counts()
print(segment_dist)
print(f'\nSegment Percentages:')
print((segment_dist / len(rfm_data) * 100).round(2))

# Segment Analysis
print('\n[5] SEGMENT CHARACTERISTICS')

segment_analysis = rfm_data.groupby('Segment').agg({
    'Recency': ['mean', 'min', 'max'],
    'Frequency': ['mean', 'min', 'max'],
    'Monetary': ['mean', 'min', 'max', 'sum'],
    'customer_id': 'count'
}).round(0)

print('\nDetailed Segment Analysis:')
for segment in rfm_data['Segment'].unique():
    segment_data = rfm_data[rfm_data['Segment'] == segment]
    print(f'\n{segment}:')
    print(f'  Count: {len(segment_data)}')
    print(f'  Avg Recency: {segment_data["Recency"].mean():.0f} days')
    print(f'  Avg Frequency: {segment_data["Frequency"].mean():.1f} transactions')
    print(f'  Avg Monetary: Rp {segment_data["Monetary"].mean():,.0f}')
    print(f'  Total Monetary: Rp {segment_data["Monetary"].sum():,.0f}')
    print(f'  % of Total Revenue: {(segment_data["Monetary"].sum() / rfm_data["Monetary"].sum() * 100):.1f}%')

# K-Means Clustering
print('\n[6] K-MEANS CLUSTERING (Optimal Segments: 4)')

X = rfm_data[['Recency', 'Frequency', 'Monetary']].copy()

# Standardization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Method Analysis
inertias = []
for k in range(1, 6):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

print('\nInertia Values (Elbow Method):')
for k, inertia in enumerate(inertias, 1):
    print(f'  K={k}: {inertia:.2f}')

print('\nOptimal clusters: 4 (based on elbow method)')

# Apply K-Means with k=4
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm_data['Cluster'] = kmeans.fit_predict(X_scaled)

print('\nCluster Distribution:')
print(rfm_data['Cluster'].value_counts().sort_index())

print('\n[7] CLUSTER CHARACTERISTICS')

for cluster in sorted(rfm_data['Cluster'].unique()):
    cluster_data = rfm_data[rfm_data['Cluster'] == cluster]
    print(f'\nCluster {cluster}:')
    print(f'  Size: {len(cluster_data)} customers')
    print(f'  Avg Recency: {cluster_data["Recency"].mean():.0f} days')
    print(f'  Avg Frequency: {cluster_data["Frequency"].mean():.1f} transactions')
    print(f'  Avg Monetary: Rp {cluster_data["Monetary"].mean():,.0f}')
    print(f'  Total Revenue: Rp {cluster_data["Monetary"].sum():,.0f}')

print('\n' + '='*80)
print('SEGMENTATION COMPLETE')
print('='*80)

print('\nRECOMMENDATIONS BY SEGMENT:')
print('\n1. CHAMPIONS (Segment: Champions, Cluster: High Value High Frequency)')
print('   - Strategy: VIP treatment, exclusive offers, loyalty programs')
print('   - Action: Premium customer support, early access to new products')
print('   - Target: Maximize retention and lifetime value')

print('\n2. LOYAL CUSTOMERS (Segment: Loyal Customers, Cluster: Frequent Buyers)')
print('   - Strategy: Engagement, cross-selling, upselling')
print('   - Action: Personalized recommendations, loyalty rewards')
print('   - Target: Increase order value')

print('\n3. BIG SPENDERS (Segment: Big Spenders, Cluster: High Monetary Low Frequency)')
print('   - Strategy: Frequency improvement, bundle offers')
print('   - Action: Tailored promotions, volume discounts')
print('   - Target: Increase purchase frequency')

print('\n4. AT RISK (Segment: At Risk, Cluster: Declining Engagement)')
print('   - Strategy: Win-back campaigns, incentive programs')
print('   - Action: Targeted discounts, personalized communication')
print('   - Target: Prevent churn')

print('\n5. LOST CUSTOMERS (Segment: Lost Customers, Cluster: Inactive)')
print('   - Strategy: Re-engagement campaigns, survey for feedback')
print('   - Action: Special comeback offers, brand refresh')
print('   - Target: Minimize acquisition cost for new customers')
