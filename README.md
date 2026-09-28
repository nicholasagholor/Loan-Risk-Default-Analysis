Loan Risk & Default Analysis Dashboard
1. Project Title

Loan Risk & Default Analysis Dashboard

An interactive Streamlit dashboard for analyzing loan applications, customer characteristics, loan risk, and default behavior.

2. Business Problem

Financial institutions need to understand the characteristics of their loan applicants and identify factors associated with loan defaults.

A high level of loan default can result in financial losses and increased credit risk. Therefore, analyzing loan application data can help identify patterns in customer demographics, credit scores, income, loan amounts, debt-to-income ratios, and other factors that may be associated with default behavior.

This project uses historical loan application data to explore these patterns and present the results through an interactive dashboard.

3. Project Objective

The main objectives of this project are to:

Analyze loan application data.
Understand the characteristics of loan applicants.
Identify patterns in loan default behavior.
Examine the relationship between credit score, income, loan amount, and default status.
Create meaningful analytical categories such as Age Group, Income Group, Credit Score Category, and Loan Size Category.
Calculate important loan risk KPIs.
Build an interactive dashboard using Streamlit.
Present findings in a clear and user-friendly format.


4. Dataset Description

The dataset contains information about loan applications and applicants.

The dataset contains 148,670 loan records and includes variables related to:

Applicant Information
Age
Gender
Income
Credit Score
Credit Type
Loan Information
Loan Amount
Loan Purpose
Loan Type
Loan Limit
Loan Term
Interest Rate
Upfront Charges
Financial Risk Information
Loan-to-Value Ratio (LTV)
Debt-to-Income Ratio (DTI)
Interest Rate Spread
Credit Worthiness
Default Status
Property Information
Property Value
Occupancy Type
Construction Type
Total Units
Security Type

The Status column is used to identify loan outcomes:

0 = Non-Defaulted
1 = Defaulted


5. Tools Used

The following tools and technologies were used in this project:

Python

Used for data cleaning, analysis, transformation, and dashboard development.

Pandas

Used for:

Loading the dataset
Data cleaning
Handling missing values
Removing duplicates
Data transformation
Grouping and aggregation
Creating analytical columns


Plotly

Used to create interactive charts and visualizations.

Streamlit

Used to build the interactive web dashboard.

VS Code

Used as the main development environment.

Git & GitHub

Used for version control and project documentation.


6. Project Procedure

The project was completed through the following stages.

Step 1: Data Loading

The loan dataset was loaded into Python using Pandas.

import pandas as pd

df = pd.read_csv("Loan_Default.csv")


Step 2: Data Exploration

The dataset was examined to understand:

Number of rows and columns
Column names
Data types
Statistical summaries
Unique categorical values
Missing values

Examples of functions used include:
df.head
df.shape
df.columns
df.dtypes
df.describe()
df.isna().sum()
df.nunique()

Step 3: Data Cleaning

The dataset was checked for:

Missing values
Duplicate records
Duplicate Loan IDs
Incorrect data types
Inconsistent categorical values

Numerical missing values were handled using appropriate statistical replacement methods such as median imputation.

Categorical missing values were handled using  mode imputation.

Step 4: Duplicate Check

Duplicate rows and Loan IDs were checked.

The ID column contains unique loan identifiers, and duplicate Loan IDs were not identified.

Step 5: Feature Engineering

New analytical columns were created to make the analysis easier to understand.

These included:

Age Group

Applicants were grouped into categories such as:

18–25
26–35
36–45
46–55
56+
Income Group

Applicants were categorized according to their income levels.

Credit Score Category

Applicants were grouped according to their credit score.

Loan Size Category

Loans were classified into categories such as:

Small Loan
Medium Loan
Large Loan
Very Large Loan

These analytical variables make it easier to compare loan behavior across different customer groups.

Step 6: Exploratory Data Analysis

The data was analyzed to identify patterns involving:

Loan defaults
Credit scores
Income
Age
Loan amounts
Loan purposes
Loan types
Property values
Loan-to-value ratio
Debt-to-income ratio


Step 7: KPI Development

Key performance indicators were created for the dashboard, including:

Total Loans
Defaulted Loans
Non-Defaulted Loans
Default Rate

The KPIs respond to the selected dashboard filters.

Step 8: Dashboard Development

An interactive dashboard was developed using Streamlit.

The dashboard includes:

Sidebar filters
KPI cards
Interactive charts
Customer and loan segmentation
Default analysis

Users can interact with the filters to explore different groups of loan applicants.

Step 9: Dashboard Testing

The dashboard was tested to ensure that:

Filters work correctly.
KPI values update when filters are applied.
Charts respond to filtered data.
The application runs successfully in Streamlit.

7. Important Findings

The analysis provides several useful insights into loan applications and default behavior.

Loan Volume

The dataset contains 148,670 loan applications, providing a large sample for analyzing loan and customer characteristics.

Default Behavior

The dashboard calculates the number of defaulted and non-defaulted loans and uses these values to calculate the overall default rate.

Credit Risk

Credit score is an important variable for understanding differences in borrower risk. The dashboard allows loan applications to be examined across different credit score categories.

Income

Income segmentation makes it possible to compare loan behavior across different income groups and examine whether default patterns differ between income categories.

Loan Size

Loan Size Category provides another way to examine whether default behavior differs between smaller and larger loans.

Customer Demographics

Age Group analysis allows customer behavior to be compared across different age ranges.

Interactive Analysis

The dashboard allows users to combine different filters and investigate specific customer and loan segments rather than relying only on overall averages.

Note: The exact KPI values and detailed patterns displayed in the dashboard depend on the filters selected by the user.

8. Recommendations

Based on the analysis, financial institutions can consider the following approaches:

1. Strengthen Risk Assessment

Use borrower characteristics such as credit score, income, loan amount, LTV, and DTI as part of a broader credit-risk assessment process.

2. Monitor High-Risk Segments

Segments showing higher observed default rates should receive closer monitoring and further investigation.

3. Use Data-Driven Loan Decisions

Historical loan data can be used to support more consistent and evidence-based lending decisions.

4. Monitor Loan Size

Loan amounts should be considered alongside the applicant's financial characteristics rather than evaluated independently.

5. Continue Monitoring Default Trends

Default rates should be monitored regularly to identify changes in borrower risk and loan performance.

6. Combine Multiple Risk Indicators

No single variable should be used as the sole basis for determining borrower risk. Credit score, income, DTI, LTV, loan amount, and other relevant factors should be considered together.

9. Instructions for Running the Streamlit Dashboard
Step 1: Install Python

Make sure Python is installed on your computer.

Step 2: Open the Project in VS Code

Open the project folder in VS Code.

The project should contain files such as:

Loan Project/
│
├── app.py
├── loan_dataset.csv
└── README.md
Step 3: Install Required Libraries

Open the VS Code terminal and run:

pip install pandas plotly streamlit
Step 4: Run the Streamlit Application

In the terminal, run:

streamlit run app.py
Step 5: Open the Dashboard

Streamlit will provide a local address, usually:

http://localhost:8501

Open the address in your web browser.

Step 6: Interact With the Dashboard

Use the sidebar filters to explore the loan data.

You can filter the dashboard based on available categories such as:

Age Group
Income Group
Credit Score Category
Loan Size Category
Loan Purpose


The KPI cards and visualizations will update based on the selected filters.

10. Project Structure
Loan Risk Analysis/
│
├── app.py
├── loan_dataset.csv
├── README.md
└── requirements.txt
11. Conclusion

This project demonstrates how Python, Pandas, Plotly, and Streamlit can be used to transform raw loan application data into an interactive risk analysis dashboard.

The dashboard provides an accessible way to examine loan volume, default behavior, customer characteristics, and different risk-related variables.

The project also demonstrates the complete data analytics workflow, from data cleaning and exploratory analysis to feature engineering, visualization, dashboard development, and business recommendations.