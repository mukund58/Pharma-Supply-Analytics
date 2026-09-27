import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Configuration
# --------------------------------------------------
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# --------------------------------------------------
# Database connection
# --------------------------------------------------

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_data(query, params=None):
    conn = get_connection()

    try:
        return pd.read_sql(
            query,
            conn,
            params=params
        )
    finally:
        conn.close()


# --------------------------------------------------
# Streamlit configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Pharma Supply Analytics",
    page_icon="💊",
    layout="wide",
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("💊 Pharma Supply Analytics")
st.caption("FDA Drug Supply & Availability Dashboard")


# --------------------------------------------------
# Load summary data
# --------------------------------------------------

status_df = load_data("""
    SELECT *
    FROM supply_status_summary
    ORDER BY records DESC;
""")


availability_df = load_data("""
    SELECT *
    FROM current_availability_summary
    ORDER BY records DESC;
""")


# --------------------------------------------------
# KPI values
# --------------------------------------------------

total_records = int(status_df["records"].sum())

current_records = int(
    status_df.loc[
        status_df["status"] == "Current",
        "records"
    ].iloc[0]
)

available_records = int(
    availability_df.loc[
        availability_df["availability"] == "Available",
        "records"
    ].iloc[0]
)

unavailable_records = int(
    availability_df.loc[
        availability_df["availability"] == "Unavailable",
        "records"
    ].iloc[0]
)


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "Current Records",
        f"{current_records:,}"
    )

with col3:
    st.metric(
        "Available",
        f"{available_records:,}"
    )

with col4:
    st.metric(
        "Unavailable",
        f"{unavailable_records:,}"
    )


st.divider()


# --------------------------------------------------
# Current Availability Chart
# --------------------------------------------------

st.subheader("Current Supply Availability")

fig = px.pie(
    availability_df,
    names="availability",
    values="records",
    hole=0.45,
)

fig.update_layout(
    showlegend=True,
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Yearly Trend + Dosage Form
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)


# --------------------------------------------------
# Records by Year
# --------------------------------------------------

with col1:

    st.subheader("Supply Records by Year")

    yearly_df = load_data("""
        SELECT
            EXTRACT(YEAR FROM initial_posting_date)::int AS year,
            COUNT(*) AS records
        FROM drug_supply_events
        GROUP BY year
        ORDER BY year;
    """)

    fig_year = px.bar(
        yearly_df,
        x="year",
        y="records",
        labels={
            "year": "Year",
            "records": "Supply Records"
        },
    )

    fig_year.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


# --------------------------------------------------
# Dosage Form
# --------------------------------------------------

with col2:

    st.subheader("Current Products by Dosage Form")

    dosage_df = load_data("""
        SELECT
            dosage_form,
            current_products
        FROM current_dosage_summary
        ORDER BY current_products DESC;
    """)

    fig_dosage = px.bar(
        dosage_df,
        x="current_products",
        y="dosage_form",
        orientation="h",
        labels={
            "current_products": "Current Products",
            "dosage_form": "Dosage Form"
        },
    )

    fig_dosage.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        yaxis=dict(
            categoryorder="total ascending"
        ),
    )

    st.plotly_chart(
        fig_dosage,
        use_container_width=True
    )

# --------------------------------------------------
# Company Analysis
# --------------------------------------------------

st.divider()

st.subheader("Company Analysis")

company_df = load_data("""
    SELECT
        c.company_name,
        COUNT(*) AS current_records
    FROM drug_supply_events e
    JOIN companies c
        ON e.company_id = c.company_id
    WHERE e.status = 'Current'
    GROUP BY c.company_name
    ORDER BY current_records DESC
    LIMIT 10;
""")


fig_company = px.bar(
    company_df,
    x="current_records",
    y="company_name",
    orientation="h",
    labels={
        "current_records": "Current Records",
        "company_name": "Company"
    },
)

fig_company.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(
    fig_company,
    use_container_width=True
)
# --------------------------------------------------
# Company Availability Analysis
# --------------------------------------------------

st.subheader("Company Availability")

all_companies = load_data("""
    SELECT DISTINCT company_name
    FROM companies
    ORDER BY company_name;
""")


selected_company = st.selectbox(
    "Select a company",
    all_companies["company_name"].tolist()
)


company_availability_df = load_data(
    """
    SELECT
        availability,
        COUNT(*) AS records
    FROM drug_supply_events e
    JOIN companies c
        ON e.company_id = c.company_id
    WHERE e.status = 'Current'
      AND c.company_name = %s
    GROUP BY availability
    ORDER BY records DESC;
    """,
    params=[selected_company]
)
fig_company_availability = px.bar(
    company_availability_df,
    x="availability",
    y="records",
    labels={
        "availability": "Availability",
        "records": "Records"
    },
)

fig_company_availability.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(
    fig_company_availability,
    use_container_width=True
)

