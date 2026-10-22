# Retail Sales & Customer Intelligence Dashboard

An interactive data analytics dashboard built using Python, Pandas, Streamlit, and Plotly to explore retail sales performance and customer behavior.

## Project Overview

This project analyzes retail transaction data to identify sales trends, evaluate profitability, compare regional and category performance, and generate actionable business insights.

## Features

- Key performance indicators for sales and profitability
- Sales and profit trend analysis
- Category-wise and regional sales analysis
- Profitability analysis by subcategory
- Customer segment distribution
- Shipping performance analysis
- Top products by sales and profit
- Discount analysis
- Business insights and searchable transaction data
- CSV export functionality

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly

## Project Structure

```text
Retail-Sales-Customer-Intelligence-Dashboard/
├── dashboard/
│   └── app.py
├── data/
│   └── superstore_clean.csv
├── notebooks/
├── import_data.py
├── README.md
└── requirements.txt
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tanvid12/Retail-Sales-Customer-Intelligence-Dashboard.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Retail-Sales-Customer-Intelligence-Dashboard
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the dashboard:

   ```bash
   python -m streamlit run dashboard/app.py
   ```

6. Open the local URL displayed in the terminal.

## Dataset

The dashboard uses a cleaned retail Superstore dataset stored in the `data/` directory.

## Purpose

The project demonstrates data cleaning, exploratory data analysis, interactive visualization, and business-oriented interpretation of retail sales data.