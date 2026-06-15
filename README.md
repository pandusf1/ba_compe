# Business Analyst Competition - Sample Project

## Deskripsi Proyek

Proyek ini merupakan contoh lengkap untuk Business Analyst Competition yang mencakup:
- Dataset e-commerce kompleks dengan multiple dimensions
- Exploratory Data Analysis (EDA)
- Customer Segmentation Analysis
- SQL queries untuk data extraction
- Business insights dan recommendations
- Visualisasi data

## Struktur Folder

```
ba_compe/
├── README.md                          # Project overview
├── data/
│   ├── sales_data.csv                # Main dataset
│   ├── customer_info.csv             # Customer demographics
│   └── product_catalog.csv           # Product information
├── notebooks/
│   ├── 01_exploratory_analysis.py    # EDA dan data profiling
│   ├── 02_customer_segmentation.py   # RFM & clustering analysis
│   └── 03_churn_prediction.py        # Predictive analytics
├── sql/
│   └── queries.sql                   # SQL templates untuk analysis
├── reports/
│   ├── business_insights.md          # Executive summary
│   └── recommendations.md            # Strategic recommendations
└── visualizations/
    └── charts.py                      # Visualization templates
```

## Business Case

**PT Digital Commerce Indonesia** - Platform e-commerce yang ingin mengoptimalkan:
1. Customer lifetime value (CLV)
2. Churn rate reduction
3. Cross-selling opportunities
4. Inventory optimization
5. Marketing campaign effectiveness

## Dataset Overview

### sales_data.csv
- **Records**: 50,000+ transactions
- **Period**: Jan 2022 - Dec 2024
- **Columns**: 
  - transaction_id, customer_id, product_id
  - order_date, purchase_amount, quantity
  - payment_method, region, product_category
  - discount_applied, return_status

### customer_info.csv
- customer_id, customer_name, email
- registration_date, lifetime_value
- customer_segment, acquisition_channel

### product_catalog.csv
- product_id, product_name, category
- price, cost, stock_level
- supplier_id, rating

## Quick Start

### 1. Setup Environment
```bash
pip install pandas numpy matplotlib seaborn scikit-learn sqlalchemy
```

### 2. Run Analysis
```bash
python notebooks/01_exploratory_analysis.py
python notebooks/02_customer_segmentation.py
python notebooks/03_churn_prediction.py
```

### 3. Check Reports
Lihat file di `reports/` untuk business insights dan recommendations

## Key Findings (Preview)

### Customer Insights
- **Churn Rate**: 28% YoY (target: reduce to 20%)
- **Top Segment**: Premium customers = 45% revenue, 15% volume
- **Avg CLV**: Rp 8.5M (range: Rp 500K - Rp 150M)

### Product Insights
- **Top Categories**: Electronics (35%), Fashion (28%), Home & Living (22%)
- **Best Performers**: 20% products = 80% revenue (Pareto principle)
- **Slow Movers**: 1,200 SKUs with <5 transactions/year

### Revenue Opportunities
- Cross-sell potential: +15% revenue
- Retention improvement: +8-10% bottom line
- Dynamic pricing: +5-7% margin optimization

## Competition Tasks

### Task 1: Customer Segmentation
**Objective**: Identify distinct customer segments for targeted marketing
- Use RFM model (Recency, Frequency, Monetary)
- Apply K-means clustering
- Define segment characteristics
- Recommend segment-specific strategies

### Task 2: Churn Prediction
**Objective**: Predict high-risk churn customers
- Build predictive model (Random Forest / XGBoost)
- Feature engineering from transaction history
- Identify churn drivers
- Propose retention strategies

### Task 3: Revenue Optimization
**Objective**: Maximize revenue through strategic initiatives
- Analyze pricing elasticity
- Identify cross-sell opportunities
- Optimize product mix
- Recommend promotional strategies

## Tools & Technologies

- **Data Processing**: Python (Pandas, NumPy)
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Machine Learning**: Scikit-learn, XGBoost
- **Database**: SQL (SQLite/PostgreSQL)
- **Documentation**: Markdown

## Author

Business Analyst Competition Sample

## License

MIT License
