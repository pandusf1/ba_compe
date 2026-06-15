import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print('='*80)
print('EXPLORATORY DATA ANALYSIS - E-Commerce Sales Data')
print('='*80)

# Load datasets
print('\n[1] Loading Data...')
sales_df = pd.read_csv('../data/sales_data.csv')
customer_df = pd.read_csv('../data/customer_info.csv')
product_df = pd.read_csv('../data/product_catalog.csv')

print(f'Sales records: {len(sales_df)}')
print(f'Unique customers: {len(customer_df)}')
print(f'Unique products: {len(product_df)}')

# Data Cleaning
print('\n[2] Data Cleaning & Preprocessing...')
sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
sales_df['year_month'] = sales_df['order_date'].dt.to_period('M')

# Basic Statistics
print('\n[3] SALES DATA OVERVIEW')
print('\nBasic Statistics:')
print(sales_df[['purchase_amount', 'quantity', 'discount_applied']].describe())

print('\nPayment Methods Distribution:')
print(sales_df['payment_method'].value_counts())

print('\nRegions Distribution:')
print(sales_df['region'].value_counts())

print('\nProduct Categories Distribution:')
print(sales_df['product_category'].value_counts())

print('\nReturn Status:')
print(sales_df['return_status'].value_counts())
return_rate = (sales_df['return_status'] == 'Yes').sum() / len(sales_df) * 100
print(f'Return Rate: {return_rate:.2f}%')

# Revenue Analysis
print('\n[4] REVENUE ANALYSIS')
total_revenue = sales_df['purchase_amount'].sum()
avg_order_value = sales_df['purchase_amount'].mean()
median_order_value = sales_df['purchase_amount'].median()

print(f'Total Revenue: Rp {total_revenue:,.0f}')
print(f'Average Order Value: Rp {avg_order_value:,.0f}')
print(f'Median Order Value: Rp {median_order_value:,.0f}')
print(f'Min Order Value: Rp {sales_df["purchase_amount"].min():,.0f}')
print(f'Max Order Value: Rp {sales_df["purchase_amount"].max():,.0f}')

# Revenue by Category
print('\nRevenue by Product Category:')
revenue_by_category = sales_df.groupby('product_category')['purchase_amount'].agg(['sum', 'count', 'mean'])
revenue_by_category.columns = ['Total Revenue', 'Transaction Count', 'Avg Order Value']
revenue_by_category['Revenue %'] = (revenue_by_category['Total Revenue'] / total_revenue * 100).round(2)
print(revenue_by_category)

# Revenue by Region
print('\nRevenue by Region:')
revenue_by_region = sales_df.groupby('region')['purchase_amount'].agg(['sum', 'count', 'mean'])
revenue_by_region.columns = ['Total Revenue', 'Transaction Count', 'Avg Order Value']
revenue_by_region['Revenue %'] = (revenue_by_region['Total Revenue'] / total_revenue * 100).round(2)
print(revenue_by_region)

# Discount Analysis
print('\n[5] DISCOUNT IMPACT ANALYSIS')
print('\nDiscount Distribution:')
print(sales_df['discount_applied'].describe())

avg_order_with_discount = sales_df[sales_df['discount_applied'] > 0]['purchase_amount'].mean()
avg_order_no_discount = sales_df[sales_df['discount_applied'] == 0]['purchase_amount'].mean()

print(f'\nAvg Order with Discount (>0%): Rp {avg_order_with_discount:,.0f}')
print(f'Avg Order without Discount: Rp {avg_order_no_discount:,.0f}')
print(f'Discount Impact: {((avg_order_with_discount - avg_order_no_discount) / avg_order_no_discount * 100):.2f}%')

# Customer Analysis
print('\n[6] CUSTOMER ANALYSIS')
print('\nCustomer Lifetime Value Statistics:')
print(customer_df['lifetime_value'].describe())

print('\nCustomers by Acquisition Channel:')
print(customer_df['acquisition_channel'].value_counts())

print('\nTop 5 Customers by Lifetime Value:')
top_customers = customer_df.nlargest(5, 'lifetime_value')[['customer_id', 'customer_name', 'lifetime_value', 'total_purchases']]
print(top_customers.to_string(index=False))

# Product Performance
print('\n[7] PRODUCT PERFORMANCE')
product_sales = sales_df.groupby('product_id').agg({
    'purchase_amount': ['sum', 'count', 'mean'],
    'quantity': 'sum'
}).round(0)
product_sales.columns = ['Revenue', 'Transactions', 'Avg Price', 'Units Sold']
product_sales = product_sales.sort_values('Revenue', ascending=False)

print('\nTop 10 Products by Revenue:')
print(product_sales.head(10))

print('\nBottom 5 Products by Revenue:')
print(product_sales.tail(5))

# Time Series Analysis
print('\n[8] TIME SERIES ANALYSIS')
monthly_revenue = sales_df.groupby('year_month')['purchase_amount'].agg(['sum', 'count', 'mean'])
monthly_revenue.columns = ['Total Revenue', 'Transaction Count', 'Avg Order Value']
print('\nMonthly Revenue Trend:')
print(monthly_revenue)

print('\n' + '='*80)
print('ANALYSIS COMPLETE')
print('='*80)
print('\nKey Takeaways:')
print('1. Overall return rate indicates product quality and customer satisfaction')
print('2. Category mix shows opportunity for cross-selling')
print('3. Regional performance suggests need for localized marketing')
print('4. Discount strategy impact on order values should be optimized')
print('5. Top customers represent significant revenue concentration')
