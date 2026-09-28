import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Loan Risk & Default Analysis Dashboard",
    layout = "wide"
)

st.title("Loan Risk & Default Analysis Dashboard")
st.write("Analysis of Loan Applications, customer risk and default behaviour")

@st.cache_data
def load_data():

    df=pd.read_csv("cleaned_loan_credit.csv")

    return df
df = load_data()


# Create Age Group
def create_age_group(age):
    if age == "<25":
        return "18-25"
    elif age == "25-34":
        return "26-35"
    elif age == "35-44":
        return "36-45"
    elif age == "45-54":
        return "46-55"
    elif age in ["55-64", "65-74", ">74"]:
        return "56+"

df["Age_Group"] = df["age"].apply(create_age_group)



df["Income_Group"] = pd.qcut(
    df["income"],
    q=4,
    labels=[
        "Low Income",
        "Middle Income",
        "High Income",
        "Very High Income"
    ]
)

st.success("Dataset loaded successfully!")

st.write("Number of rows:", df.shape[0])

st.write("Number of columns:", df.shape[1])

def credit_category(score):
    if score < 580:
        return "Poor"
    elif score < 670:
        return "Fair"
    elif score < 740:
        return "Good"
    elif score < 800:
        return "Very Good"
    else:
        return "Excellent"

df["credit_score_category"] = df["Credit_Score"].apply(
    credit_category
)

df["Loan_Size_Category"] = pd.qcut(
    df["loan_amount"],
    q=4,
    labels=[
        "Small Loan",
        "Medium Loan",
        "Large Loan",
        "Very Large Loan"
    ]
)


df["DTI_Category"] = pd.qcut(
    df["dtir1"],
    q=4,
    labels=[
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)


df["Interest_Rate_Group"] = pd.qcut(
    df["rate_of_interest"],
    q=4,
    labels=[
        "Low Interest",
        "Moderate Interest",
        "High Interest",
        "Very High Interest"
    ]
)

df["Loan_Term_Group"] = pd.cut(
    df["term"],
    bins=[0, 180, 240, 300, 360],
    labels=[
        "Up to 180 Months",
        "181-240 Months",
        "241-300 Months",
        "301-360 Months"
    ],
    include_lowest=True
)

# Create LTV Group
df["LTV_Group"] = pd.qcut(
    df["LTV"],
    q=4,
    labels=[
        "Low LTV",
        "Moderate LTV",
        "High LTV",
        "Very High LTV"
    ]
)


df["Loan_to_Income"] = (
    df["loan_amount"] / df["income"]
)




st.subheader("Analytical Columns")

st.write(
    df[
        [
            "Age_Group",
            "Income_Group",
            "credit_score_category",
            "Loan_Size_Category",
            "DTI_Category"
        ]
    ].head()
)


st.sidebar.title("Dashboard")

st.sidebar.write(
    "Use the filters below to explore loan applications, "
    "customer risk, and default behaviour."
)

page = st.sidebar.radio(
    "Select Page",
    [
        "Executive Overview",
        "Customer Risk Analysis",
        "Loan Analysis",
        "Customer Profile Analysis"
    ]
)

st.sidebar.subheader("Filters")

selected_status = st.sidebar.selectbox(
    "Loan Status",
    ["All Loans", "Defaulted Loans", "Non-Defaulted Loans"],
    key="loan_status"
)

selected_purpose = st.sidebar.multiselect(
    "Loan Purpose",
    options=df["loan_purpose"].dropna().unique(),
    default=df["loan_purpose"].dropna().unique(),
    key="loan_purpose"
)


selected_age = st.sidebar.multiselect(
    "Select Age Group",
    ["18-25", "26-35", "36-45", "46-55", "56+"],
    default=["18-25", "26-35", "36-45", "46-55", "56+"],
    key="age_group"
)


st.sidebar.subheader("Income Group")

selected_income = st.sidebar.multiselect(
    "Select Income Group",
    [
        "Low Income",
        "Middle Income",
        "High Income",
        "Very High Income"
    ],
    default=[
        "Low Income",
        "Middle Income",
        "High Income",
        "Very High Income"
    ],
    key="income_group"
)


selected_credit = st.sidebar.multiselect(
    "Credit Score Category",
    ["Poor", "Fair", "Good", "Very Good", "Excellent"],
    default=["Poor", "Fair", "Good", "Very Good", "Excellent"],
    key="credit_score"
)


selected_loan_size = st.sidebar.multiselect(
    "Loan Size Category",
    ["Small Loan", "Medium Loan", "Large Loan", "Very Large Loan"],
    default=["Small Loan", "Medium Loan", "Large Loan", "Very Large Loan"],
    key="loan_size"
)

if st.sidebar.button("Reset Filters"):
    st.session_state["loan_purpose"] = df["loan_purpose"].dropna().unique().tolist()

    st.session_state["age_group"] = [
        "18-25", "26-35", "36-45", "46-55", "56+"
    ]

    st.session_state["income_group"] = [
        "Low Income",
        "Middle Income",
        "High Income",
        "Very High Income"
    ]

    st.session_state["credit_score"] = [
        "Poor",
        "Fair",
        "Good",
        "Very Good",
        "Excellent"
    ]

    st.session_state["loan_size"] = [
        "Small Loan",
        "Medium Loan",
        "Large Loan",
        "Very Large Loan"
    ]

    st.session_state["loan_status"] = "All Loans"

    st.rerun()

    st.sidebar.markdown("---")

st.sidebar.subheader("About This Dashboard")

st.sidebar.write(
    "This dashboard analyzes loan applications, "
    "customer characteristics, risk levels, and loan default behaviour."
)




income_low_threshold = df["income"].quantile(0.25)
loan_high_threshold = df["loan_amount"].quantile(0.75)
interest_high_threshold = df["rate_of_interest"].quantile(0.75)

df["Risk_Score"] = (
    (df["Credit_Score"] < 670).astype(int)
    + (df["dtir1"] > 43).astype(int)
    + (df["income"] < income_low_threshold).astype(int)
    + (df["loan_amount"] > loan_high_threshold).astype(int)
    + (df["rate_of_interest"] > interest_high_threshold).astype(int)
)


def classify_risk(score):
    if score <= 1:
        return "Low Risk"
    elif score <= 3:
        return "Moderate Risk"
    else:
        return "High Risk"


df["Risk_Category"] = df["Risk_Score"].apply(classify_risk)

filtered_df = df[
    (df["loan_purpose"].isin(selected_purpose)) &
    (df["Age_Group"].isin(selected_age)) &
    (df["Income_Group"].isin(selected_income)) &
    (df["credit_score_category"].isin(selected_credit)) &
    (df["Loan_Size_Category"].isin(selected_loan_size))
]

if selected_status == "Defaulted Loans":
    filtered_df = filtered_df[filtered_df["Status"] == 1]

elif selected_status == "Non-Defaulted Loans":
    filtered_df = filtered_df[filtered_df["Status"] == 0]

    
csv_data = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="filtered_loan_data.csv",
    mime="text/csv"
)

if page == "Executive Overview":
    st.header("Executive Overview")

    # KPI CARDS
    total_loans = len(filtered_df)
    defaulted_loans = (filtered_df["Status"] == 1).sum()
    non_defaulted_loans = (filtered_df["Status"] == 0).sum()

    if total_loans > 0:
        default_rate = (defaulted_loans / total_loans) * 100
    else:
        default_rate = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Loans", total_loans)
    col2.metric("Defaulted Loans", defaulted_loans)
    col3.metric("Non-Defaulted Loans", non_defaulted_loans)
    col4.metric("Default Rate", f"{default_rate:.2f}%")


    
    default_data = pd.DataFrame({
        "Status": ["Non-Defaulted", "Defaulted"],
        "Number of Loans": [
            non_defaulted_loans,
            defaulted_loans
        ]
    })

    fig = px.bar(
        default_data,
        x="Status",
        y="Number of Loans",
        title="Defaulted vs Non-Defaulted Loans",
        text="Number of Loans"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Loan Status",
        yaxis_title="Number of Loans",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="default_status_chart"
    )


    
    age_data = (
        filtered_df["Age_Group"]
        .value_counts()
        .reindex(["18-25", "26-35", "36-45", "46-55", "56+"])
        .reset_index()
    )

    age_data.columns = ["Age Group", "Number of Loans"]

    fig_age = px.bar(
        age_data,
        x="Age Group",
        y="Number of Loans",
        title="Loans by Age Group",
        text="Number of Loans"
    )

    fig_age.update_traces(
        textposition="outside"
    )

    fig_age.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Number of Loans",
        height=450
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True,
        key="loans_by_age_group"
    )


    
    purpose_data = (
        filtered_df["loan_purpose"]
        .value_counts()
        .reset_index()
    )

    purpose_data.columns = ["Loan Purpose", "Number of Loans"]

    fig_purpose = px.bar(
        purpose_data,
        x="Loan Purpose",
        y="Number of Loans",
        title="Loans by Loan Purpose",
        text="Number of Loans"
    )

    fig_purpose.update_traces(
        textposition="outside"
    )

    fig_purpose.update_layout(
        xaxis_title="Loan Purpose",
        yaxis_title="Number of Loans",
        height=450
    )

    st.plotly_chart(
        fig_purpose,
        use_container_width=True,
        key="loans_by_purpose"
    )

elif page == "Customer Risk Analysis":
    st.header("Customer Risk Analysis")
    st.write(
        "Analysis of customer characteristics and their relationship with loan default."
    )

    age_default = (
        filtered_df.groupby("Age_Group", observed=True)["Status"]
        .mean()
        .reindex(["18-25", "26-35", "36-45", "46-55", "56+"])
        .reset_index()
    )

    age_default["Default Rate"] = age_default["Status"] * 100

    fig_age_default = px.bar(
        age_default,
        x="Age_Group",
        y="Default Rate",
        title="Default Rate by Age Group",
        text="Default Rate"
    )

    fig_age_default.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_age_default.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_age_default,
        use_container_width=True,
        key="default_rate_by_age"
    )


       
    income_default = (
        filtered_df.groupby("Income_Group", observed=True)["Status"]
        .mean()
        .reset_index()
    )

    income_default["Default Rate"] = income_default["Status"] * 100

    fig_income_default = px.bar(
        income_default,
        x="Income_Group",
        y="Default Rate",
        title="Default Rate by Income Group",
        text="Default Rate"
    )

    fig_income_default.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_income_default.update_layout(
        xaxis_title="Income Group",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_income_default,
        use_container_width=True,
        key="default_rate_by_income"
    )

        
    credit_default = (
        filtered_df.groupby(
            "credit_score_category",
            observed=True
        )["Status"]
        .mean()
        .reset_index()
    )

    credit_default["Default Rate"] = credit_default["Status"] * 100

    fig_credit_default = px.bar(
        credit_default,
        x="credit_score_category",
        y="Default Rate",
        title="Default Rate by Credit Score Category",
        text="Default Rate"
    )

    fig_credit_default.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_credit_default.update_layout(
        xaxis_title="Credit Score Category",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_credit_default,
        use_container_width=True,
        key="default_rate_by_credit"
    )

        # Default Rate by DTI Category
    dti_default = (
        filtered_df.groupby(
            "DTI_Category",
            observed=True
        )["Status"]
        .mean()
        .reset_index()
    )

    dti_default["Default Rate"] = dti_default["Status"] * 100

    fig_dti_default = px.bar(
        dti_default,
        x="DTI_Category",
        y="Default Rate",
        title="Default Rate by DTI Category",
        text="Default Rate"
    )

    fig_dti_default.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_dti_default.update_layout(
        xaxis_title="DTI Category",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_dti_default,
        use_container_width=True,
        key="default_rate_by_dti"
    )

       
    risk_default = (
        filtered_df.groupby(
            "Risk_Category",
            observed=True
        )
        .agg(
            Total_Loans=("Status", "count"),
            Total_Defaults=("Status", "sum"),
            Default_Rate=("Status", "mean")
        )
        .reset_index()
    )

    risk_default["Default Rate"] = risk_default["Default_Rate"] * 100

    fig_risk = px.bar(
        risk_default,
        x="Risk_Category",
        y="Default Rate",
        title="Default Rate by Risk Category",
        text="Default Rate"
    )

    fig_risk.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_risk.update_layout(
        xaxis_title="Risk Category",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        key="default_rate_by_risk"
    )

    
    st.subheader("Risk Category Summary")

    st.dataframe(
        risk_default[
            [
                "Risk_Category",
                "Total_Loans",
                "Total_Defaults",
                "Default Rate"
            ]
        ],
        use_container_width=True
    )

elif page == "Loan Analysis":
    st.header("Loan Analysis")
    st.write(
        "Analysis of loan characteristics, loan size, purpose, interest rate, term, and LTV."
    )

        
    loan_size_default = (
        filtered_df.groupby(
            "Loan_Size_Category",
            observed=True
        )["Status"]
        .mean()
        .reset_index()
    )

    loan_size_default["Default Rate"] = (
        loan_size_default["Status"] * 100
    )

    fig_loan_size = px.bar(
        loan_size_default,
        x="Loan_Size_Category",
        y="Default Rate",
        title="Default Rate by Loan Size Category",
        text="Default Rate"
    )

    fig_loan_size.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_loan_size.update_layout(
        xaxis_title="Loan Size Category",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_loan_size,
        use_container_width=True,
        key="default_rate_by_loan_size"
    )


        
    purpose_loan_amount = (
        filtered_df.groupby("loan_purpose")
        .agg(
            Average_Loan_Amount=("loan_amount", "mean"),
            Median_Loan_Amount=("loan_amount", "median")
        )
        .reset_index()
    )

    fig_purpose_amount = px.bar(
        purpose_loan_amount,
        x="loan_purpose",
        y="Average_Loan_Amount",
        title="Average Loan Amount by Loan Purpose",
        text="Average_Loan_Amount"
    )

    fig_purpose_amount.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_purpose_amount.update_layout(
        xaxis_title="Loan Purpose",
        yaxis_title="Average Loan Amount",
        height=450
    )

    st.plotly_chart(
        fig_purpose_amount,
        use_container_width=True,
        key="average_loan_by_purpose"
    )


        
    interest_default = (
        filtered_df.groupby("Interest_Rate_Group", observed=True)["Status"]
        .mean()
        .reset_index()
    )

    interest_default["Default Rate"] = (
        interest_default["Status"] * 100
    )

    fig_interest = px.bar(
        interest_default,
        x="Interest_Rate_Group",
        y="Default Rate",
        title="Default Rate by Interest Rate Group",
        text="Default Rate"
    )

    fig_interest.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_interest.update_layout(
        xaxis_title="Interest Rate Group",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_interest,
        use_container_width=True,
        key="default_rate_by_interest"
    )

    
    term_default = (
    filtered_df.groupby(
        "Loan_Term_Group",
        observed=True
    )["Status"]
    .mean()
    .reset_index())

    term_default["Default Rate"] = (
    term_default["Status"] * 100)

    fig_term = px.bar(
    term_default,
    x="Loan_Term_Group",
    y="Default Rate",
    title="Default Rate by Loan Term",
    text="Default Rate")

    fig_term.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside")

    fig_term.update_layout(
    xaxis_title="Loan Term",
    yaxis_title="Default Rate (%)",
    height=450)

    st.plotly_chart(
    fig_term,
    use_container_width=True,
    key="default_rate_by_term")

    # Default Rate by LTV Group
    ltv_default = (
    filtered_df.groupby(
        "LTV_Group",
        observed=True
    )["Status"]
    .mean()
    .reset_index())

    ltv_default["Default Rate"] = (
    ltv_default["Status"] * 100)

    fig_ltv = px.bar(
    ltv_default,
    x="LTV_Group",
    y="Default Rate",
    title="Default Rate by LTV Group",
    text="Default Rate"
)

    fig_ltv.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside")

    fig_ltv.update_layout(
    xaxis_title="LTV Group",
    yaxis_title="Default Rate (%)",
    height=450)

    st.plotly_chart(
    fig_ltv,
    use_container_width=True,
    key="default_rate_by_ltv")


    
    fig_loan_income = px.histogram(
    filtered_df,
    x="Loan_to_Income",
    nbins=50,
    title="Loan-to-Income Ratio Distribution")

    fig_loan_income.update_layout(
    xaxis_title="Loan-to-Income Ratio",
    yaxis_title="Number of Loans",
    height=450)

    st.plotly_chart(
    fig_loan_income,
    use_container_width=True,
    key="loan_to_income_distribution")

elif page == "Customer Profile Analysis":
    st.header("Customer Profile Analysis")

    st.write(
        "Analysis of customer demographic and profile characteristics."
    )

       
    gender_default = (
        filtered_df.groupby("Gender")["Status"]
        .mean()
        .reset_index()
    )

    gender_default["Default Rate"] = (
        gender_default["Status"] * 100
    )

    fig_gender = px.bar(
        gender_default,
        x="Gender",
        y="Default Rate",
        title="Default Rate by Gender",
        text="Default Rate"
    )

    fig_gender.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_gender.update_layout(
        xaxis_title="Gender",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True,
        key="default_rate_by_gender"
    )


        # Default Rate by Region
    region_default = (
        filtered_df.groupby("Region")["Status"]
        .mean()
        .reset_index()
    )

    region_default["Default Rate"] = (
        region_default["Status"] * 100
    )

    fig_region = px.bar(
        region_default,
        x="Region",
        y="Default Rate",
        title="Default Rate by Region",
        text="Default Rate"
    )

    fig_region.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True,
        key="default_rate_by_region"
    )

        
    credit_type_default = (
        filtered_df.groupby("credit_type")["Status"]
        .mean()
        .reset_index()
    )

    credit_type_default["Default Rate"] = (
        credit_type_default["Status"] * 100
    )

    fig_credit_type = px.bar(
        credit_type_default,
        x="credit_type",
        y="Default Rate",
        title="Default Rate by Credit Type",
        text="Default Rate"
    )

    fig_credit_type.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_credit_type.update_layout(
        xaxis_title="Credit Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_credit_type,
        use_container_width=True,
        key="default_rate_by_credit_type"
    )


        
    occupancy_default = (
        filtered_df.groupby("occupancy_type")["Status"]
        .mean()
        .reset_index()
    )

    occupancy_default["Default Rate"] = (
        occupancy_default["Status"] * 100
    )

    fig_occupancy = px.bar(
        occupancy_default,
        x="occupancy_type",
        y="Default Rate",
        title="Default Rate by Occupancy Type",
        text="Default Rate"
    )

    fig_occupancy.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_occupancy.update_layout(
        xaxis_title="Occupancy Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_occupancy,
        use_container_width=True,
        key="default_rate_by_occupancy"
    )


        
    coapplicant_default = (
        filtered_df.groupby("co-applicant_credit_type")["Status"]
        .mean()
        .reset_index()
    )

    coapplicant_default["Default Rate"] = (
        coapplicant_default["Status"] * 100
    )

    fig_coapplicant = px.bar(
        coapplicant_default,
        x="co-applicant_credit_type",
        y="Default Rate",
        title="Default Rate by Co-Applicant Credit Type",
        text="Default Rate"
    )

    fig_coapplicant.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_coapplicant.update_layout(
        xaxis_title="Co-Applicant Credit Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_coapplicant,
        use_container_width=True,
        key="default_rate_by_coapplicant"
    )

        
    loan_type_default = (
        filtered_df.groupby("loan_type")["Status"]
        .mean()
        .reset_index()
    )

    loan_type_default["Default Rate"] = (
        loan_type_default["Status"] * 100
    )

    fig_loan_type = px.bar(
        loan_type_default,
        x="loan_type",
        y="Default Rate",
        title="Default Rate by Loan Type",
        text="Default Rate"
    )

    fig_loan_type.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_loan_type.update_layout(
        xaxis_title="Loan Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_loan_type,
        use_container_width=True,
        key="default_rate_by_loan_type"
    )


        
    construction_default = (
        filtered_df.groupby("construction_type")["Status"]
        .mean()
        .reset_index()
    )

    construction_default["Default Rate"] = (
        construction_default["Status"] * 100
    )

    fig_construction = px.bar(
        construction_default,
        x="construction_type",
        y="Default Rate",
        title="Default Rate by Construction Type",
        text="Default Rate"
    )

    fig_construction.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_construction.update_layout(
        xaxis_title="Construction Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_construction,
        use_container_width=True,
        key="default_rate_by_construction"
    )

        
    security_default = (
        filtered_df.groupby("Security_Type")["Status"]
        .mean()
        .reset_index()
    )

    security_default["Default Rate"] = (
        security_default["Status"] * 100
    )

    fig_security = px.bar(
        security_default,
        x="Security_Type",
        y="Default Rate",
        title="Default Rate by Security Type",
        text="Default Rate"
    )

    fig_security.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_security.update_layout(
        xaxis_title="Security Type",
        yaxis_title="Default Rate (%)",
        height=450
    )

    st.plotly_chart(
        fig_security,
        use_container_width=True,
        key="default_rate_by_security"
    )


       
    st.subheader("Customer Profile Summary")

    profile_summary = (
        filtered_df.groupby("Gender")["Status"]
        .agg(
            Total_Loans="count",
            Total_Defaults="sum",
            Default_Rate="mean"
        )
        .reset_index()
    )

    profile_summary["Default_Rate"] = (
        profile_summary["Default_Rate"] * 100
    )

    profile_summary["Default_Rate"] = (
        profile_summary["Default_Rate"].round(2)
    )

    st.dataframe(
        profile_summary,
        use_container_width=True
    )



    st.markdown("---")

st.caption(
    "Loan Risk & Default Analysis Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)

