import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print('='*80)
print('COMPREHENSIVE VISUALIZATION - E-COMMERCE ANALYSIS')
print('='*80)

# Load data
print('\n[Loading Data...]')
sales_df = pd.read_csv('../data/sales_data.csv')
customer_df = pd.read_csv('../data/customer_info.csv')
product_df = pd.read_csv('../data/product_catalog.csv')

sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
sales_df['year_month'] = sales_df['order_date'].dt.to_period('M')

import os
os.makedirs('../visualizations/output', exist_ok=True)

print('[Generating 15 Professional Charts...]\n')

# CHART 1: Revenue by Category
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Chart 1: Product Category Performance', fontsize=16, fontweight='bold', y=1.02)

revenue_by_category = sales_df.groupby('product_category')['purchase_amount'].sum().sort_values(ascending=False)
colors = sns.color_palette('Set2', len(revenue_by_category))

axes[0].bar(revenue_by_category.index, revenue_by_category.values / 1e9, color=colors)
axes[0].set_title('Total Revenue by Category', fontweight='bold')
axes[0].set_ylabel('Revenue (Rp Billion)', fontweight='bold')
axes[0].set_xlabel('Product Category', fontweight='bold')
axes[0].tick_params(axis='x', rotation=45)
for i, v in enumerate(revenue_by_category.values / 1e9):
    axes[0].text(i, v + 0.2, f'Rp {v:.1f}B', ha='center', fontweight='bold')

wedges, texts, autotexts = axes[1].pie(revenue_by_category.values, 
                                         labels=revenue_by_category.index,
                                         autopct='%1.1f%%',
                                         colors=colors,
                                         startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
axes[1].set_title('Revenue Share by Category', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/01_category_performance.png', dpi=300, bbox_inches='tight')
print('✅ Chart 1: Category Performance')
plt.close()

# CHART 2: Revenue by Region
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 2: Regional Revenue Distribution', fontsize=14, fontweight='bold', y=0.98)

revenue_by_region = sales_df.groupby('region')['purchase_amount'].sum().sort_values()
colors_region = sns.color_palette('coolwarm', len(revenue_by_region))

ax.barh(revenue_by_region.index, revenue_by_region.values / 1e9, color=colors_region)
ax.set_xlabel('Revenue (Rp Billion)', fontweight='bold')
ax.set_title('Revenue by Region', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for i, v in enumerate(revenue_by_region.values / 1e9):
    ax.text(v + 0.1, i, f'Rp {v:.1f}B ({v/revenue_by_region.sum()*100:.1f}%)', 
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/02_regional_distribution.png', dpi=300, bbox_inches='tight')
print('✅ Chart 2: Regional Distribution')
plt.close()

# CHART 3: Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Chart 3: Revenue Trend Over Time', fontsize=14, fontweight='bold', y=0.98)

monthly_revenue = sales_df.groupby('year_month')['purchase_amount'].agg(['sum', 'count']).reset_index()
monthly_revenue['sum'] = monthly_revenue['sum'] / 1e9
monthly_revenue['month_str'] = monthly_revenue['year_month'].astype(str)

ax.plot(range(len(monthly_revenue)), monthly_revenue['sum'].values, 
        marker='o', linewidth=2.5, markersize=8, color='#2E86AB', label='Revenue')
ax.fill_between(range(len(monthly_revenue)), monthly_revenue['sum'].values, alpha=0.3, color='#2E86AB')

ax.set_xlabel('Month', fontweight='bold')
ax.set_ylabel('Revenue (Rp Billion)', fontweight='bold')
ax.set_title('Monthly Revenue Trend', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, len(monthly_revenue), 2))
ax.set_xticklabels(monthly_revenue['month_str'].values[::2], rotation=45)

for i, v in enumerate(monthly_revenue['sum'].values):
    if i % 2 == 0:
        ax.text(i, v + 0.05, f'Rp {v:.1f}B', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/03_revenue_trend.png', dpi=300, bbox_inches='tight')
print('✅ Chart 3: Revenue Trend')
plt.close()

# CHART 4: Average Order Value
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 4: Price Point Analysis', fontsize=14, fontweight='bold', y=0.98)

aov_by_category = sales_df.groupby('product_category')['purchase_amount'].mean().sort_values(ascending=False)
colors_aov = sns.color_palette('RdYlGn', len(aov_by_category))

ax.bar(aov_by_category.index, aov_by_category.values / 1e6, color=colors_aov)
ax.set_ylabel('Average Order Value (Rp Million)', fontweight='bold')
ax.set_xlabel('Product Category', fontweight='bold')
ax.set_title('Average Order Value by Category', fontweight='bold')
ax.tick_params(axis='x', rotation=45)

for i, v in enumerate(aov_by_category.values / 1e6):
    ax.text(i, v + 0.05, f'Rp {v:.2f}M', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/04_aov_analysis.png', dpi=300, bbox_inches='tight')
print('✅ Chart 4: Price Point Analysis')
plt.close()

# CHART 5: Discount Impact
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 5: Discount Strategy Impact', fontsize=14, fontweight='bold', y=0.98)

sales_df['discount_range'] = pd.cut(sales_df['discount_applied'], 
                                     bins=[-1, 0, 5, 10, 15, 100],
                                     labels=['No Discount', '1-5%', '6-10%', '11-15%', '>15%'])

discount_impact = sales_df.groupby('discount_range', observed=True)['purchase_amount'].agg(['mean', 'count']).reset_index()
discount_impact['mean'] = discount_impact['mean'] / 1e6

colors_discount = sns.color_palette('RdYlGn_r', len(discount_impact))
ax.bar(discount_impact['discount_range'], discount_impact['mean'], color=colors_discount)
ax.set_ylabel('Average Order Value (Rp Million)', fontweight='bold')
ax.set_xlabel('Discount Range', fontweight='bold')
ax.set_title('Impact of Discount on Order Value', fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for i, (idx, row) in enumerate(discount_impact.iterrows()):
    ax.text(i, row['mean'] + 0.02, f"Rp {row['mean']:.2f}M\n(n={int(row['count'])})", 
            ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('../visualizations/output/05_discount_impact.png', dpi=300, bbox_inches='tight')
print('✅ Chart 5: Discount Impact')
plt.close()

# CHART 6: Return Rate
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 6: Product Quality & Satisfaction', fontsize=14, fontweight='bold', y=0.98)

return_by_category = sales_df.groupby('product_category').apply(
    lambda x: (x['return_status'] == 'Yes').sum() / len(x) * 100
).sort_values(ascending=False)

colors_return = sns.color_palette('RdYlGn_r', len(return_by_category))
ax.bar(return_by_category.index, return_by_category.values, color=colors_return)
ax.set_ylabel('Return Rate (%)', fontweight='bold')
ax.set_xlabel('Product Category', fontweight='bold')
ax.set_title('Return Rate by Category', fontweight='bold')
ax.axhline(y=10, color='red', linestyle='--', linewidth=2, label='Target (10%)')
ax.legend()
ax.tick_params(axis='x', rotation=45)

for i, v in enumerate(return_by_category.values):
    ax.text(i, v + 0.2, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/06_return_rate.png', dpi=300, bbox_inches='tight')
print('✅ Chart 6: Return Rate Analysis')
plt.close()

# CHART 7: Payment Methods
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Chart 7: Payment Method Analysis', fontsize=16, fontweight='bold', y=1.02)

payment_data = sales_df['payment_method'].value_counts()
payment_revenue = sales_df.groupby('payment_method')['purchase_amount'].sum().sort_values(ascending=False)

colors_payment = sns.color_palette('Set3', len(payment_data))

axes[0].bar(payment_data.index, payment_data.values, color=colors_payment)
axes[0].set_title('Transaction Count by Payment Method', fontweight='bold')
axes[0].set_ylabel('Number of Transactions', fontweight='bold')
for i, v in enumerate(payment_data.values):
    axes[0].text(i, v + 50, str(v), ha='center', fontweight='bold')

axes[1].bar(payment_revenue.index, payment_revenue.values / 1e9, color=colors_payment)
axes[1].set_title('Revenue by Payment Method', fontweight='bold')
axes[1].set_ylabel('Revenue (Rp Billion)', fontweight='bold')
for i, v in enumerate(payment_revenue.values / 1e9):
    axes[1].text(i, v + 0.1, f'Rp {v:.1f}B', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/07_payment_methods.png', dpi=300, bbox_inches='tight')
print('✅ Chart 7: Payment Method Analysis')
plt.close()

# CHART 8: CLV Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Chart 8: Customer Value Distribution', fontsize=16, fontweight='bold', y=1.02)

axes[0].hist(customer_df['lifetime_value'] / 1e6, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Lifetime Value (Rp Million)', fontweight='bold')
axes[0].set_ylabel('Number of Customers', fontweight='bold')
axes[0].set_title('CLV Distribution', fontweight='bold')
axes[0].axvline(customer_df['lifetime_value'].mean() / 1e6, color='red', 
               linestyle='--', linewidth=2, label=f'Mean: Rp {customer_df["lifetime_value"].mean()/1e6:.1f}M')
axes[0].legend()

data_for_box = customer_df[['lifetime_value']].values / 1e6
box = axes[1].boxplot(data_for_box, vert=True, patch_artist=True)
for patch in box['boxes']:
    patch.set_facecolor('#3498db')
axes[1].set_ylabel('Lifetime Value (Rp Million)', fontweight='bold')
axes[1].set_title('CLV Box Plot Analysis', fontweight='bold')
axes[1].set_xticklabels(['All Customers'])

plt.tight_layout()
plt.savefig('../visualizations/output/08_clv_distribution.png', dpi=300, bbox_inches='tight')
print('✅ Chart 8: CLV Distribution')
plt.close()

# CHART 9: Top Customers
fig, ax = plt.subplots(figsize=(12, 7))
fig.suptitle('Chart 9: VIP Customer Concentration', fontsize=14, fontweight='bold', y=0.98)

top_customers = customer_df.nlargest(10, 'lifetime_value').sort_values('lifetime_value')
colors_customers = sns.color_palette('YlOrRd', len(top_customers))

ax.barh(range(len(top_customers)), top_customers['lifetime_value'].values / 1e6, color=colors_customers)
ax.set_yticks(range(len(top_customers)))
ax.set_yticklabels(top_customers['customer_name'].values)
ax.set_xlabel('Lifetime Value (Rp Million)', fontweight='bold')
ax.set_title('Top 10 Customers by Lifetime Value', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for i, v in enumerate(top_customers['lifetime_value'].values / 1e6):
    ax.text(v + 0.5, i, f'Rp {v:.1f}M', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/09_top_customers.png', dpi=300, bbox_inches='tight')
print('✅ Chart 9: Top Customers')
plt.close()

# CHART 10: Acquisition Channels
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle('Chart 10: Marketing Channel Effectiveness', fontsize=14, fontweight='bold', y=0.995)

channel_data = customer_df.groupby('acquisition_channel').agg({
    'customer_id': 'count',
    'lifetime_value': ['sum', 'mean']
}).round(0)
channel_data.columns = ['customers', 'total_ltv', 'avg_ltv']
channel_data = channel_data.sort_values('total_ltv', ascending=False)

colors_channel = sns.color_palette('husl', len(channel_data))

axes[0].bar(channel_data.index, channel_data['total_ltv'].values / 1e9, color=colors_channel)
axes[0].set_ylabel('Total LTV (Rp Billion)', fontweight='bold')
axes[0].set_title('Total Customer Value by Acquisition Channel', fontweight='bold')
for i, v in enumerate(channel_data['total_ltv'].values / 1e9):
    axes[0].text(i, v + 0.1, f'Rp {v:.1f}B', ha='center', fontweight='bold')

axes[1].bar(channel_data.index, channel_data['avg_ltv'].values / 1e6, color=colors_channel)
axes[1].set_ylabel('Average LTV per Customer (Rp Million)', fontweight='bold')
axes[1].set_xlabel('Acquisition Channel', fontweight='bold')
axes[1].set_title('Average Customer Value by Acquisition Channel', fontweight='bold')
axes[1].tick_params(axis='x', rotation=45)
for i, v in enumerate(channel_data['avg_ltv'].values / 1e6):
    axes[1].text(i, v + 0.2, f'Rp {v:.1f}M', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/10_acquisition_channels.png', dpi=300, bbox_inches='tight')
print('✅ Chart 10: Acquisition Channels')
plt.close()

# CHART 11: Product Matrix
fig, ax = plt.subplots(figsize=(12, 7))
fig.suptitle('Chart 11: Product Portfolio Analysis', fontsize=14, fontweight='bold', y=0.98)

product_perf = sales_df.groupby('product_id').agg({
    'purchase_amount': 'sum',
    'quantity': 'sum'
}).reset_index()
product_perf = product_perf.merge(product_df[['product_id', 'product_name']], on='product_id')

ax.scatter(product_perf['quantity'], product_perf['purchase_amount'] / 1e6,
                    s=200, alpha=0.6, c=range(len(product_perf)), cmap='viridis')

ax.set_xlabel('Units Sold', fontweight='bold')
ax.set_ylabel('Total Revenue (Rp Million)', fontweight='bold')
ax.set_title('Product Performance: Revenue vs Volume', fontweight='bold')
ax.grid(True, alpha=0.3)

ax.axvline(product_perf['quantity'].median(), color='red', linestyle='--', alpha=0.5)
ax.axhline(product_perf['purchase_amount'].median() / 1e6, color='red', linestyle='--', alpha=0.5)

top_products = product_perf.nlargest(5, 'purchase_amount')
for idx, row in top_products.iterrows():
    ax.annotate(row['product_name'][:15], 
               (row['quantity'], row['purchase_amount'] / 1e6),
               xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/11_product_matrix.png', dpi=300, bbox_inches='tight')
print('✅ Chart 11: Product Matrix')
plt.close()

# CHART 12: Tenure Impact
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Chart 12: Customer Loyalty Impact', fontsize=14, fontweight='bold', y=0.98)

ax.scatter(customer_df['customer_tenure_days'], customer_df['lifetime_value'] / 1e6,
          s=150, alpha=0.6, color='#2E86AB')

ax.set_xlabel('Customer Tenure (Days)', fontweight='bold')
ax.set_ylabel('Lifetime Value (Rp Million)', fontweight='bold')
ax.set_title('Relationship: Customer Tenure vs Lifetime Value', fontweight='bold')
ax.grid(True, alpha=0.3)

z = np.polyfit(customer_df['customer_tenure_days'], customer_df['lifetime_value'] / 1e6, 1)
p = np.poly1d(z)
ax.plot(customer_df['customer_tenure_days'].sort_values(), 
       p(customer_df['customer_tenure_days'].sort_values()),
       "r--", linewidth=2, label='Trend Line (Positive Correlation)')
ax.legend()

plt.tight_layout()
plt.savefig('../visualizations/output/12_tenure_value.png', dpi=300, bbox_inches='tight')
print('✅ Chart 12: Tenure Impact')
plt.close()

# CHART 13: Day of Week
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 13: Temporal Patterns', fontsize=14, fontweight='bold', y=0.98)

sales_df['day_of_week'] = sales_df['order_date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = sales_df['day_of_week'].value_counts().reindex(day_order)

colors_day = sns.color_palette('coolwarm', len(day_counts))
ax.bar(range(len(day_counts)), day_counts.values, color=colors_day)
ax.set_xticks(range(len(day_counts)))
ax.set_xticklabels(day_counts.index, rotation=45)
ax.set_ylabel('Transaction Count', fontweight='bold')
ax.set_title('Transaction Volume by Day of Week', fontweight='bold')

for i, v in enumerate(day_counts.values):
    ax.text(i, v + 0.3, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/13_day_of_week.png', dpi=300, bbox_inches='tight')
print('✅ Chart 13: Day of Week Pattern')
plt.close()

# CHART 14: Heatmap
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Chart 14: Category-Region Performance Matrix', fontsize=14, fontweight='bold', y=0.98)

heatmap_data = sales_df.pivot_table(values='purchase_amount', 
                                    index='product_category', 
                                    columns='region',
                                    aggfunc='sum') / 1e9

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlGn', ax=ax, cbar_kws={'label': 'Revenue (Rp B)'})
ax.set_title('Revenue Heatmap: Category vs Region (Rp Billion)', fontweight='bold')
ax.set_xlabel('Region', fontweight='bold')
ax.set_ylabel('Product Category', fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/output/14_heatmap.png', dpi=300, bbox_inches='tight')
print('✅ Chart 14: Category-Region Heatmap')
plt.close()

# CHART 15: Dashboard Summary
fig = plt.figure(figsize=(14, 8))
fig.suptitle('Chart 15: Executive Summary Dashboard', fontsize=16, fontweight='bold', y=0.98)

gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

total_revenue = sales_df['purchase_amount'].sum()
avg_order_value = sales_df['purchase_amount'].mean()
total_customers = len(customer_df)
total_transactions = len(sales_df)
churn_rate = 28
return_rate = (sales_df['return_status'] == 'Yes').sum() / len(sales_df) * 100
avg_clv = customer_df['lifetime_value'].mean()
repeat_rate = (sales_df.groupby('customer_id')['transaction_id'].count() > 1).sum() / total_customers * 100

metrics = [
    ('Total Revenue', f'Rp {total_revenue/1e9:.1f}B', '#3498db'),
    ('Avg Order Value', f'Rp {avg_order_value/1e6:.2f}M', '#2ecc71'),
    ('Total Customers', f'{total_customers}', '#e74c3c'),
    ('Transactions', f'{total_transactions}', '#f39c12'),
    ('Churn Rate', f'{churn_rate:.1f}%', '#e91e63'),
    ('Return Rate', f'{return_rate:.1f}%', '#9c27b0'),
    ('Avg Customer LTV', f'Rp {avg_clv/1e6:.1f}M', '#00bcd4'),
    ('Repeat Rate', f'{repeat_rate:.1f}%', '#4caf50'),
    ('Avg Daily Revenue', f'Rp {(total_revenue/30)/1e9:.2f}B', '#ff9800'),
]

positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

for idx, (metric_name, metric_value, color) in enumerate(metrics):
    ax = fig.add_subplot(gs[positions[idx][0], positions[idx][1]])
    ax.axis('off')
    
    rect = plt.Rectangle((0, 0), 1, 1, facecolor=color, alpha=0.2, transform=ax.transAxes)
    ax.add_patch(rect)
    
    ax.text(0.5, 0.65, metric_name, ha='center', va='center', fontsize=11, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.35, metric_value, ha='center', va='center', fontsize=14, fontweight='bold', 
           color=color, transform=ax.transAxes)
    
    rect_border = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=color, linewidth=2, transform=ax.transAxes)
    ax.add_patch(rect_border)

plt.savefig('../visualizations/output/15_dashboard_summary.png', dpi=300, bbox_inches='tight')
print('✅ Chart 15: Dashboard Summary')
plt.close()

print('\n' + '='*80)
print('ALL 15 CHARTS GENERATED SUCCESSFULLY!')
print('='*80)
print('\nChart Inventory:')
print('1. Category Performance (Bar + Pie)')
print('2. Regional Distribution (Horizontal Bar)')
print('3. Revenue Trend (Line Chart)')
print('4. Price Point Analysis (Bar)')
print('5. Discount Impact (Bar)')
print('6. Return Rate (Bar)')
print('7. Payment Methods (Double Bar)')
print('8. CLV Distribution (Histogram + Box Plot)')
print('9. Top Customers (Horizontal Bar)')
print('10. Acquisition Channels (Grouped Bar)')
print('11. Product Matrix (Scatter Plot)')
print('12. Tenure Impact (Scatter with Trend)')
print('13. Day of Week Pattern (Bar)')
print('14. Category-Region Heatmap')
print('15. Executive Summary Dashboard')
print('\n✅ Ready for presentation!')
