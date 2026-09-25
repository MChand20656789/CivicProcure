import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DB_FILE = BASE_DIR / "output" / "civicprocure.db"


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="CivicProcure",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# Database helper
# ---------------------------------------------------------

@st.cache_data
def load_data():

    connection = sqlite3.connect(DB_FILE)

    submissions = pd.read_sql_query(
        """
        SELECT *
        FROM procurement_submissions
        """,
        connection,
    )

    validation = pd.read_sql_query(
        """
        SELECT *
        FROM validation_results
        """,
        connection,
    )

    feedback = pd.read_sql_query(
        """
        SELECT *
        FROM stakeholder_feedback
        """,
        connection,
    )

    vendors = pd.read_sql_query(
        """
        SELECT *
        FROM vendors
        """,
        connection,
    )

    connection.close()

    return (
        submissions,
        validation,
        feedback,
        vendors,
    )


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

try:

    (
        submissions,
        validation,
        feedback,
        vendors,
    ) = load_data()

except Exception as error:

    st.error(
        f"Unable to load CivicProcure database: {error}"
    )

    st.stop()


# ---------------------------------------------------------
# Data preparation
# ---------------------------------------------------------

submissions["requested_amount"] = pd.to_numeric(
    submissions["requested_amount"],
    errors="coerce",
)

submissions["approved_amount"] = pd.to_numeric(
    submissions["approved_amount"],
    errors="coerce",
)

submissions["review_days"] = pd.to_numeric(
    submissions["review_days"],
    errors="coerce",
)


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("CivicProcure")

st.subheader(
    "Procurement Operations Analytics System"
)

st.caption(
    "Simulated procurement operations environment "
    "using fictional data for portfolio demonstration."
)


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------

st.sidebar.header("Filters")

agency_options = sorted(
    submissions["agency"].dropna().unique()
)

selected_agencies = st.sidebar.multiselect(
    "Agency",
    options=agency_options,
    default=agency_options,
)


status_options = sorted(
    submissions["status"].dropna().unique()
)

selected_statuses = st.sidebar.multiselect(
    "Status",
    options=status_options,
    default=status_options,
)


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------

filtered = submissions[
    submissions["agency"].isin(selected_agencies)
    & submissions["status"].isin(selected_statuses)
].copy()


# ---------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------

total_submissions = len(filtered)

pending = filtered[
    filtered["status"].isin(
        ["Pending", "Under Review"]
    )
].shape[0]

average_review_days = (
    filtered["review_days"].mean()
    if not filtered.empty
    else 0
)

follow_up_ids = validation[
    validation["submission_id"].isin(
        filtered["submission_id"]
    )
]["submission_id"].nunique()


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Submissions",
        f"{total_submissions:,}",
    )

with col2:

    st.metric(
        "Pending / Under Review",
        f"{pending:,}",
    )

with col3:

    st.metric(
        "Avg Review Time",
        f"{average_review_days:.1f} days",
    )

with col4:

    st.metric(
        "Requiring Follow-Up",
        f"{follow_up_ids:,}",
    )


st.divider()


# ---------------------------------------------------------
# Row 1 — Procurement volume
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Procurement Volume by Agency"
    )

    agency_volume = (
        filtered.groupby("agency")
        .size()
        .reset_index(
            name="submission_count"
        )
        .sort_values(
            "submission_count",
            ascending=False,
        )
    )

    fig = px.bar(
        agency_volume,
        x="agency",
        y="submission_count",
        labels={
            "agency": "Agency",
            "submission_count": "Submissions",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
        height=400,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with col2:

    st.subheader(
        "Average Review Time by Agency"
    )

    review_by_agency = (
        filtered.groupby("agency")
        .agg(
            average_review_days=(
                "review_days",
                "mean",
            )
        )
        .reset_index()
        .sort_values(
            "average_review_days",
            ascending=False,
        )
    )

    review_by_agency[
        "average_review_days"
    ] = review_by_agency[
        "average_review_days"
    ].round(1)

    fig = px.bar(
        review_by_agency,
        x="agency",
        y="average_review_days",
        labels={
            "agency": "Agency",
            "average_review_days":
                "Average Review Days",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
        height=400,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ---------------------------------------------------------
# Row 2 — Issues
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Validation Issues by Category"
    )

    if not validation.empty:

        issue_counts = (
            validation[
                validation["submission_id"].isin(
                    filtered["submission_id"]
                )
            ]
            .groupby("check")
            .size()
            .reset_index(
                name="issue_count"
            )
            .sort_values(
                "issue_count",
                ascending=False,
            )
        )

        fig = px.bar(
            issue_counts,
            x="check",
            y="issue_count",
            labels={
                "check": "Validation Check",
                "issue_count": "Issues",
            },
        )

        fig.update_layout(
            xaxis_tickangle=-30,
            height=400,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info(
            "No validation issues for the selected filters."
        )


with col2:

    st.subheader(
        "Pending Submissions by Review Stage"
    )

    pending_df = filtered[
        filtered["status"].isin(
            ["Pending", "Under Review"]
        )
    ]

    stage_counts = (
        pending_df
        .groupby("review_stage")
        .size()
        .reset_index(
            name="submission_count"
        )
        .sort_values(
            "submission_count",
            ascending=False,
        )
    )

    fig = px.bar(
        stage_counts,
        x="review_stage",
        y="submission_count",
        labels={
            "review_stage": "Review Stage",
            "submission_count":
                "Pending Submissions",
        },
    )

    fig.update_layout(
        xaxis_tickangle=-30,
        height=400,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ---------------------------------------------------------
# Financial overview
# ---------------------------------------------------------

st.divider()

st.subheader(
    "Requested vs. Approved Amounts"
)

financial = (
    filtered.groupby("agency")
    .agg(
        requested_amount=(
            "requested_amount",
            "sum",
        ),
        approved_amount=(
            "approved_amount",
            "sum",
        ),
    )
    .reset_index()
)

financial_long = financial.melt(
    id_vars="agency",
    value_vars=[
        "requested_amount",
        "approved_amount",
    ],
    var_name="amount_type",
    value_name="amount",
)

financial_long["amount_type"] = (
    financial_long["amount_type"]
    .map({
        "requested_amount": "Requested",
        "approved_amount": "Approved",
    })
)

fig = px.bar(
    financial_long,
    x="agency",
    y="amount",
    color="amount_type",
    barmode="group",
    labels={
        "agency": "Agency",
        "amount": "Amount ($)",
        "amount_type": "Amount Type",
    },
)

fig.update_layout(
    xaxis_tickangle=-30,
    height=450,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# ---------------------------------------------------------
# Follow-up table
# ---------------------------------------------------------

st.divider()

st.subheader(
    "Submissions Requiring Follow-Up"
)

follow_up = filtered[
    filtered["submission_id"].isin(
        validation["submission_id"]
    )
].copy()

follow_up = follow_up[
    [
        "submission_id",
        "agency",
        "vendor_id",
        "status",
        "review_stage",
        "review_days",
        "requested_amount",
        "approved_amount",
    ]
].sort_values(
    "review_days",
    ascending=False,
)

for _, row in follow_up.iterrows():
    st.write(
        f"**{row['submission_id']}** | "
        f"{row['agency']} | "
        f"{row['vendor_id']} | "
        f"{row['status']} | "
        f"{row['review_stage']} | "
        f"{row['review_days']} days | "
        f"${row['requested_amount']:,.2f} requested | "
        f"${row['approved_amount']:,.2f} approved"
    )