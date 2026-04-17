# Expense Tracker App using Data Science

## Overview
This project is a beginner-friendly but professional finance analytics project built for students targeting Data Analyst, Business Analyst, and Financial Analyst roles. It accepts manual user input, CSV input, or synthetic sample data, then cleans it, analyzes spending behavior, creates charts, and generates business insights.

## 1. Project Explanation

### What is an Expense Tracker App?
An Expense Tracker App records expenses such as food, rent, travel, shopping, and bills. It stores transactions and turns them into meaningful summaries so a user can understand where money is going.

### Why is it important?
- It improves financial awareness.
- It helps control unnecessary spending.
- It supports budgeting and savings.
- It helps individuals and businesses make better decisions.

### How individuals and companies use it
- Individuals use it for personal finance tracking, bill planning, and spending control.
- Companies use similar systems for business expense monitoring, reimbursement management, and budget control.

### Real-world use cases
- Personal finance tracking
- Business expense monitoring
- Budgeting and cost control
- Financial planning

### Simple explanation
It is a smart system for recording expenses and understanding spending patterns.

### Technical explanation
It is a Python-based analytics pipeline that accepts manual expense entry, CSV-based input, or generated sample data, then cleans the data, performs exploratory analysis, creates visualizations, compares spend with budgets, and produces insight reports for decision-making.

### Workflow
`data input -> storage -> analysis -> visualization -> insights -> decision-making`

### Workflow explanation
- Data input: user-entered or synthetic expense records
- Storage: CSV files
- Analysis: cleaning, aggregation, and trend analysis with Pandas
- Visualization: charts with Matplotlib and Seaborn
- Insights: summary findings from the processed data
- Decision-making: budget optimization and overspending detection
- 
## 3. Project Architecture

### Input
- date
- category
- amount
- payment method
- city

### Processing
- data cleaning
- missing value handling
- duplicate removal
- categorization
- aggregation
- trend analysis
- budget comparison

### Output
- reports
- charts
- insights

### Text-based architecture diagram
```text
Synthetic Data / User Input
            |
            v
      Raw Expense Data
            |
            v
      Data Cleaning Layer
            |
            v
   Feature Engineering Layer
            |
            v
   Analysis and Aggregation
            |
            v
  Visualization and Reporting
            |
            v
  Insights and Decision Support
```

### Data flow explanation
The app first accepts expense data from manual input, CSV import, or synthetic generation. Then it cleans the dataset, derives time-based features like month and quarter, aggregates spending by category and month, compares actual spend to a budget map, and saves reports plus charts for interpretation.

## 4. Implementation Plan

### Phase 1: Setup
- What to do: create folders, install libraries, prepare environment
- Why: ensures clean and reproducible development
- Expected output: project structure and working Python environment
- Mistakes to avoid: installing packages globally instead of in a virtual environment

### Phase 2: Data creation/input
- What to do: generate synthetic transactions
- Why: real financial data is usually private
- Expected output: raw synthetic CSV
- Mistakes to avoid: generating unrealistic random values without patterns

### Phase 3: Cleaning
- What to do: fix nulls, convert dates, remove duplicates
- Why: reliable analysis needs clean data
- Expected output: cleaned CSV
- Mistakes to avoid: skipping validation after cleaning

### Phase 4: EDA
- What to do: inspect spend by category, month, and payment method
- Why: reveals patterns and anomalies
- Expected output: summary tables
- Mistakes to avoid: ignoring outliers and seasonal effects

### Phase 5: Feature engineering
- What to do: create year, month, weekday, quarter, and essential-spend fields
- Why: helps deeper analysis
- Expected output: richer analytical dataset
- Mistakes to avoid: creating features that are never used

### Phase 6: Analysis
- What to do: compute total spend, averages, trends, and budget breaches
- Why: creates business value
- Expected output: analysis CSV files
- Mistakes to avoid: reporting metrics without business meaning

### Phase 7: Visualization
- What to do: create bar, line, pie, and heatmap charts
- Why: makes patterns easier to communicate
- Expected output: PNG images
- Mistakes to avoid: unreadable labels and poor titles

### Phase 8: Insights
- What to do: generate conclusion statements from analysis
- Why: analysts are expected to explain findings
- Expected output: insights report text file
- Mistakes to avoid: vague observations with no evidence

## 5. Folder Structure

```text
Expense-Tracker-App/
|
|-- data/
|-- notebooks/
|-- src/
|-- outputs/
|-- images/
|-- README.md
|-- requirements.txt
`-- main.py
```

### Explanation
- `data/`: raw and cleaned datasets
- `notebooks/`: optional Jupyter notebooks
- `src/`: project source code
- `outputs/`: summary reports and insight files
- `images/`: graphs and screenshots
- `README.md`: project documentation
- `requirements.txt`: required Python libraries
- `main.py`: run file

## 7. Full Project Code

### `main.py`
```python
from src.expense_tracker import run_expense_tracker_project


if __name__ == "__main__":
    run_expense_tracker_project()
```

### Main implementation
The complete logic is in `src/expense_tracker.py`. It includes:
- dataset creation using synthetic expenses
- data cleaning
- category analysis
- monthly trends
- spending patterns
- visualization
- insights generation

## 8. Virtual Simulation

### How simulation works
- You can either enter expenses manually, import a CSV, or generate synthetic records.
- Categories include Food, Travel, Rent, Utilities, Shopping, Entertainment, Healthcare, Education, Subscriptions, and Miscellaneous.
- Seasonal patterns are injected so the dataset looks realistic.
- Monthly category spending is compared against a fixed budget map.
- Overspending is detected when actual monthly spend exceeds the assigned budget.

### Step-by-step simulation
1. Choose a run mode: manual input, CSV import, or synthetic sample.
2. Enter or load transaction records with date, category, amount, city, and payment method.
3. Clean the data.
4. Engineer month, quarter, weekday, and essential-spend features.
5. Aggregate category and monthly totals.
6. Compare monthly category totals with budgets.
7. Create charts.
8. Generate the final insights report.

### What screenshots to take
- raw data preview
- cleaned data preview
- category-wise bar chart
- monthly trend chart
- payment method pie chart
- monthly heatmap
- budget breach chart
- final terminal output


## 9. How to Run Project

```powershell
python main.py
```

### Expected outputs
- `data/manual_expenses_raw.csv` or `data/csv_expenses_raw.csv` or `data/synthetic_expenses_raw.csv`
- `data/manual_expenses_cleaned.csv` or `data/csv_expenses_cleaned.csv` or `data/synthetic_expenses_cleaned.csv`
- `outputs/category_summary.csv`
- `outputs/monthly_summary.csv`
- `outputs/payment_summary.csv`
- `outputs/monthly_category_budget_check.csv`
- `outputs/insights_report.txt`
- charts inside `images/`

## 15. Future Improvements
- Build a Streamlit dashboard
- Add real-time expense entry
- Add AI-based spending prediction
- Add budgeting alerts
- Add financial goal tracking
- Build a mobile app version

## Results
This project demonstrates practical data cleaning, business-focused analysis, financial reporting, and portfolio-quality documentation. It is especially useful as GitHub proof for internships and entry-level analyst roles.
