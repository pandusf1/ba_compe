-- ============================================================================
-- SQL TEMPLATES FOR BUSINESS ANALYST COMPETITION
-- E-Commerce Analysis Queries
-- ============================================================================

-- 1. BASIC SALES OVERVIEW
-- Query: Daily Revenue, Transaction Count, Average Order Value
-- Purpose: Monitor sales performance and trends
SELECT
    DATE(order_date) as order_date,
    COUNT(*) as transaction_count,
    SUM(purchase_amount) as total_revenue,
    AVG(purchase_amount) as avg_order_value,
    SUM(quantity) as total_quantity,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY DATE(order_date)
ORDER BY order_date DESC;

-- 2. CATEGORY PERFORMANCE
-- Query: Revenue contribution by product category
-- Purpose: Identify top-performing categories and growth opportunities
SELECT
    product_category,
    COUNT(*) as transaction_count,
    SUM(purchase_amount) as total_revenue,
    ROUND(SUM(purchase_amount) * 100.0 / (SELECT SUM(purchase_amount) FROM sales_data), 2) as revenue_percentage,
    AVG(purchase_amount) as avg_order_value,
    SUM(quantity) as total_units,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY product_category
ORDER BY total_revenue DESC;

-- 3. REGIONAL ANALYSIS
-- Query: Sales performance by region
-- Purpose: Identify regional strengths and expansion opportunities
SELECT
    region,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(purchase_amount) as total_revenue,
    AVG(purchase_amount) as avg_order_value,
    MAX(purchase_amount) as highest_order,
    MIN(purchase_amount) as lowest_order,
    ROUND(100.0 * SUM(CASE WHEN return_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) as return_rate_percent
FROM sales_data
GROUP BY region
ORDER BY total_revenue DESC;

-- 4. CUSTOMER VALUE ANALYSIS
-- Query: Customer Lifetime Value and Segmentation
-- Purpose: Identify high-value customers for targeted retention
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(s.transaction_id) as transaction_count,
    SUM(s.purchase_amount) as lifetime_value,
    AVG(s.purchase_amount) as avg_order_value,
    MAX(s.order_date) as last_purchase_date,
    MIN(s.order_date) as first_purchase_date,
    COUNT(DISTINCT s.product_category) as category_diversity,
    CASE
        WHEN SUM(s.purchase_amount) >= 15000000 THEN 'VIP'
        WHEN SUM(s.purchase_amount) >= 8000000 THEN 'Premium'
        WHEN SUM(s.purchase_amount) >= 4000000 THEN 'Gold'
        ELSE 'Regular'
    END as customer_segment
FROM customer_info c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY lifetime_value DESC;

-- 5. PRODUCT PERFORMANCE
-- Query: Top and bottom performing products
-- Purpose: Optimize product portfolio
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    COUNT(s.transaction_id) as sales_count,
    SUM(s.purchase_amount) as total_revenue,
    AVG(s.purchase_amount) as avg_selling_price,
    SUM(s.quantity) as units_sold,
    ROUND(100.0 * COUNT(CASE WHEN s.return_status = 'Yes' THEN 1 END) / COUNT(s.transaction_id), 2) as return_rate,
    p.stock_level as current_stock
FROM product_catalog p
LEFT JOIN sales_data s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, p.price, p.stock_level
HAVING COUNT(s.transaction_id) > 0
ORDER BY total_revenue DESC;

-- 6. DISCOUNT IMPACT ANALYSIS
-- Query: Effectiveness of discount strategy
-- Purpose: Optimize discount strategy for profitability
SELECT
    CASE
        WHEN discount_applied = 0 THEN 'No Discount'
        WHEN discount_applied <= 5 THEN '1-5%'
        WHEN discount_applied <= 10 THEN '6-10%'
        WHEN discount_applied <= 15 THEN '11-15%'
        ELSE '>15%'
    END as discount_range,
    COUNT(*) as transaction_count,
    SUM(purchase_amount) as total_revenue,
    AVG(purchase_amount) as avg_order_value,
    ROUND(100.0 * COUNT(CASE WHEN return_status = 'Yes' THEN 1 END) / COUNT(*), 2) as return_rate,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY discount_range
ORDER BY discount_applied ASC;

-- 7. PAYMENT METHOD ANALYSIS
-- Query: Customer preference and performance by payment method
-- Purpose: Optimize payment options
SELECT
    payment_method,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(purchase_amount) as total_revenue,
    AVG(purchase_amount) as avg_order_value,
    ROUND(100.0 * SUM(CASE WHEN return_status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) as return_rate_percent
FROM sales_data
GROUP BY payment_method
ORDER BY total_revenue DESC;

-- 8. CUSTOMER ACQUISITION CHANNEL ANALYSIS
-- Query: ROI and effectiveness of acquisition channels
-- Purpose: Allocate marketing budget efficiently
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) as customers_acquired,
    SUM(c.lifetime_value) as total_ltv,
    AVG(c.lifetime_value) as avg_ltv,
    COUNT(DISTINCT s.transaction_id) as total_transactions,
    SUM(s.purchase_amount) as generated_revenue
FROM customer_info c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY c.acquisition_channel
ORDER BY total_ltv DESC;

-- 9. COHORT ANALYSIS
-- Query: Analyze customer behavior by acquisition cohort
-- Purpose: Track retention and lifetime value trends
SELECT
    YEAR(c.registration_date) as registration_year,
    MONTH(c.registration_date) as registration_month,
    COUNT(DISTINCT c.customer_id) as cohort_size,
    SUM(c.lifetime_value) as cohort_ltv,
    AVG(c.lifetime_value) as avg_ltv,
    COUNT(DISTINCT s.transaction_id) as total_transactions
FROM customer_info c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY YEAR(c.registration_date), MONTH(c.registration_date)
ORDER BY registration_year DESC, registration_month DESC;

-- 10. CHURN RISK IDENTIFICATION
-- Query: Identify customers at risk of churning
-- Purpose: Implement targeted retention campaigns
SELECT
    c.customer_id,
    c.customer_name,
    c.lifetime_value,
    COUNT(s.transaction_id) as total_purchases,
    MAX(s.order_date) as last_purchase_date,
    CAST((CURRENT_DATE - MAX(s.order_date)) as INTEGER) as days_since_last_purchase,
    CASE
        WHEN CAST((CURRENT_DATE - MAX(s.order_date)) as INTEGER) > 90 THEN 'At Risk'
        WHEN CAST((CURRENT_DATE - MAX(s.order_date)) as INTEGER) > 60 THEN 'Warning'
        ELSE 'Active'
    END as churn_status
FROM customer_info c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name, c.lifetime_value
ORDER BY days_since_last_purchase DESC;

-- 11. CROSS-SELL OPPORTUNITIES
-- Query: Identify customers who haven't purchased from all categories
-- Purpose: Design targeted cross-sell campaigns
SELECT
    s.customer_id,
    COUNT(DISTINCT s.product_category) as categories_purchased,
    GROUP_CONCAT(DISTINCT s.product_category) as purchased_categories,
    SUM(s.purchase_amount) as total_spent,
    CASE
        WHEN COUNT(DISTINCT s.product_category) < 3 THEN 'High Potential'
        WHEN COUNT(DISTINCT s.product_category) = 3 THEN 'Medium Potential'
        ELSE 'Low Potential'
    END as crosssell_potential
FROM sales_data s
GROUP BY s.customer_id
HAVING COUNT(DISTINCT s.product_category) < 3
ORDER BY total_spent DESC;

-- 12. MONTHLY REVENUE FORECAST DATA
-- Query: Historical monthly metrics for forecasting
-- Purpose: Revenue projection and trend analysis
SELECT
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(purchase_amount) as revenue,
    AVG(purchase_amount) as avg_order_value,
    SUM(quantity) as units_sold,
    ROUND(100.0 * COUNT(CASE WHEN return_status = 'Yes' THEN 1 END) / COUNT(*), 2) as return_rate
FROM sales_data
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;
