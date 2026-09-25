import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

SUBMISSIONS_FILE = DATA_DIR / "procurement_submissions.csv"
VALIDATION_FILE = OUTPUT_DIR / "validation_results.csv"

METRICS_FILE = OUTPUT_DIR / "procurement_metrics.csv"
AGENCY_FILE = OUTPUT_DIR / "agency_metrics.csv"
STAGE_FILE = OUTPUT_DIR / "review_stage_metrics.csv"
ISSUE_FILE = OUTPUT_DIR / "issue_metrics.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(SUBMISSIONS_FILE)

validation = pd.read_csv(
    VALIDATION_FILE
)


# ---------------------------------------------------------
# Clean fields
# ---------------------------------------------------------

df["requested_amount"] = pd.to_numeric(
    df["requested_amount"],
    errors="coerce"
)

df["approved_amount"] = pd.to_numeric(
    df["approved_amount"],
    errors="coerce"
)

df["review_days"] = pd.to_numeric(
    df["review_days"],
    errors="coerce"
)


# ---------------------------------------------------------
# Basic operational metrics
# ---------------------------------------------------------

total_submissions = len(df)

pending_submissions = (
    df["status"]
    .isin(["Pending", "Under Review"])
    .sum()
)

approved_submissions = (
    df["status"] == "Approved"
).sum()

rejected_submissions = (
    df["status"] == "Rejected"
).sum()

average_review_days = df["review_days"].mean()

total_requested_amount = (
    df["requested_amount"]
    .sum()
)

total_approved_amount = (
    df["approved_amount"]
    .sum()
)

approval_rate = (
    approved_submissions / total_submissions
    if total_submissions
    else 0
)

submissions_requiring_followup = (
    validation["submission_id"]
    .nunique()
)

high_severity_issues = (
    validation["severity"] == "High"
).sum()

compliance_issues = (
    validation["check"]
    .isin([
        "Completeness",
        "Vendor Validation",
        "Date Validation",
        "Status Validation",
        "MWBE Validation",
    ])
).sum()


# ---------------------------------------------------------
# Overall metrics table
# ---------------------------------------------------------

metrics = pd.DataFrame([
    {
        "metric": "Total Submissions",
        "value": total_submissions,
    },
    {
        "metric": "Pending Submissions",
        "value": pending_submissions,
    },
    {
        "metric": "Approved Submissions",
        "value": approved_submissions,
    },
    {
        "metric": "Rejected Submissions",
        "value": rejected_submissions,
    },
    {
        "metric": "Average Review Days",
        "value": round(average_review_days, 2),
    },
    {
        "metric": "Total Requested Amount",
        "value": round(total_requested_amount, 2),
    },
    {
        "metric": "Total Approved Amount",
        "value": round(total_approved_amount, 2),
    },
    {
        "metric": "Approval Rate",
        "value": round(approval_rate, 4),
    },
    {
        "metric": "Submissions Requiring Follow-Up",
        "value": submissions_requiring_followup,
    },
    {
        "metric": "High Severity Issues",
        "value": high_severity_issues,
    },
    {
        "metric": "Compliance/Data Quality Issues",
        "value": compliance_issues,
    },
])

metrics.to_csv(
    METRICS_FILE,
    index=False
)


# ---------------------------------------------------------
# Agency-level metrics
# ---------------------------------------------------------

agency_metrics = (
    df.groupby("agency")
    .agg(
        submissions=("submission_id", "count"),
        requested_amount=("requested_amount", "sum"),
        approved_amount=("approved_amount", "sum"),
        average_review_days=("review_days", "mean"),
    )
    .reset_index()
)

agency_metrics["approval_rate"] = (
    df.assign(
        approved=df["status"] == "Approved"
    )
    .groupby("agency")["approved"]
    .mean()
    .values
)

agency_metrics["requested_amount"] = (
    agency_metrics["requested_amount"]
    .round(2)
)

agency_metrics["approved_amount"] = (
    agency_metrics["approved_amount"]
    .round(2)
)

agency_metrics["average_review_days"] = (
    agency_metrics["average_review_days"]
    .round(2)
)

agency_metrics.to_csv(
    AGENCY_FILE,
    index=False
)


# ---------------------------------------------------------
# Review-stage metrics
# ---------------------------------------------------------

stage_metrics = (
    df.groupby("review_stage")
    .agg(
        submissions=("submission_id", "count"),
        average_review_days=("review_days", "mean"),
    )
    .reset_index()
)

stage_metrics["average_review_days"] = (
    stage_metrics["average_review_days"]
    .round(2)
)

stage_metrics.to_csv(
    STAGE_FILE,
    index=False
)


# ---------------------------------------------------------
# Issue metrics
# ---------------------------------------------------------

if not validation.empty:

    issue_metrics = (
        validation.groupby(
            ["check", "severity"]
        )
        .size()
        .reset_index(
            name="issue_count"
        )
        .sort_values(
            "issue_count",
            ascending=False
        )
    )

else:

    issue_metrics = pd.DataFrame(
        columns=[
            "check",
            "severity",
            "issue_count",
        ]
    )


issue_metrics.to_csv(
    ISSUE_FILE,
    index=False
)


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

print()
print("CivicProcure Operational Metrics")
print("=" * 40)

print(
    f"Total submissions: "
    f"{total_submissions}"
)

print(
    f"Pending submissions: "
    f"{pending_submissions}"
)

print(
    f"Approved submissions: "
    f"{approved_submissions}"
)

print(
    f"Average review days: "
    f"{average_review_days:.2f}"
)

print(
    f"Total requested: "
    f"${total_requested_amount:,.2f}"
)

print(
    f"Total approved: "
    f"${total_approved_amount:,.2f}"
)

print(
    f"Approval rate: "
    f"{approval_rate:.1%}"
)

print(
    f"Submissions requiring follow-up: "
    f"{submissions_requiring_followup}"
)

print()
print("Output files created:")
print(METRICS_FILE)
print(AGENCY_FILE)
print(STAGE_FILE)
print(ISSUE_FILE)