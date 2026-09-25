import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

INPUT_FILE = DATA_DIR / "procurement_submissions.csv"
VENDORS_FILE = DATA_DIR / "vendors.csv"

OUTPUT_FILE = OUTPUT_DIR / "validation_results.csv"
SUMMARY_FILE = OUTPUT_DIR / "validation_summary.txt"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)
vendors = pd.read_csv(VENDORS_FILE)


# ---------------------------------------------------------
# Standardize dates
# ---------------------------------------------------------

df["submission_date"] = pd.to_datetime(
    df["submission_date"],
    errors="coerce"
)

df["contract_start_date"] = pd.to_datetime(
    df["contract_start_date"],
    errors="coerce"
)

df["contract_end_date"] = pd.to_datetime(
    df["contract_end_date"],
    errors="coerce"
)


# ---------------------------------------------------------
# Numeric fields
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
# Validation configuration
# ---------------------------------------------------------

VALID_STATUSES = {
    "Approved",
    "Pending",
    "Under Review",
    "Rejected",
}

VALID_REVIEW_STAGES = {
    "Intake",
    "Financial Review",
    "Compliance Review",
    "Legal Review",
    "Final Approval",
}

REQUIRED_FIELDS = [
    "submission_id",
    "agency",
    "vendor_id",
    "procurement_type",
    "submission_date",
    "requested_amount",
    "approved_amount",
    "contract_start_date",
    "contract_end_date",
    "status",
    "review_stage",
]


# ---------------------------------------------------------
# Create validation records
# ---------------------------------------------------------

validation_records = []


def add_issue(
    submission_id,
    check,
    result,
    severity,
    message
):
    validation_records.append({
        "submission_id": submission_id,
        "check": check,
        "result": result,
        "severity": severity,
        "message": message,
    })


# ---------------------------------------------------------
# Required-field checks
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]

    for field in REQUIRED_FIELDS:

        value = row[field]

        if pd.isna(value) or value == "":

            add_issue(
                submission_id,
                "Completeness",
                "FAIL",
                "High",
                f"Missing required field: {field}"
            )


# ---------------------------------------------------------
# Vendor validation
# ---------------------------------------------------------

valid_vendor_ids = set(
    vendors["vendor_id"].dropna()
)

for _, row in df.iterrows():

    submission_id = row["submission_id"]
    vendor_id = row["vendor_id"]

    if pd.isna(vendor_id) or vendor_id == "":

        add_issue(
            submission_id,
            "Vendor Validation",
            "FAIL",
            "High",
            "Vendor ID is missing"
        )

    elif vendor_id not in valid_vendor_ids:

        add_issue(
            submission_id,
            "Vendor Validation",
            "FAIL",
            "High",
            f"Vendor ID {vendor_id} does not exist"
        )


# ---------------------------------------------------------
# Duplicate submission detection
# ---------------------------------------------------------

duplicate_mask = df.duplicated(
    subset=["submission_id"],
    keep=False
)

for _, row in df[duplicate_mask].iterrows():

    add_issue(
        row["submission_id"],
        "Duplicate Detection",
        "FAIL",
        "High",
        "Duplicate submission ID detected"
    )


# ---------------------------------------------------------
# Financial validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]

    requested = row["requested_amount"]
    approved = row["approved_amount"]

    if pd.notna(requested) and pd.notna(approved):

        if approved > requested:

            add_issue(
                submission_id,
                "Financial Validation",
                "FAIL",
                "High",
                "Approved amount exceeds requested amount"
            )

        elif approved < 0 or requested < 0:

            add_issue(
                submission_id,
                "Financial Validation",
                "FAIL",
                "High",
                "Financial amount cannot be negative"
            )


# ---------------------------------------------------------
# Contract-date validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]

    start = row["contract_start_date"]
    end = row["contract_end_date"]

    if pd.notna(start) and pd.notna(end):

        if end <= start:

            add_issue(
                submission_id,
                "Date Validation",
                "FAIL",
                "High",
                "Contract end date must occur after start date"
            )


# ---------------------------------------------------------
# Status validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]
    status = row["status"]

    if status not in VALID_STATUSES:

        add_issue(
            submission_id,
            "Status Validation",
            "FAIL",
            "Medium",
            f"Invalid status: {status}"
        )


# ---------------------------------------------------------
# Review-stage validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]
    stage = row["review_stage"]

    if stage not in VALID_REVIEW_STAGES:

        add_issue(
            submission_id,
            "Review Stage Validation",
            "FAIL",
            "Medium",
            f"Invalid review stage: {stage}"
        )


# ---------------------------------------------------------
# MWBE validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]
    mwbe_status = row["mwbe_status"]

    if pd.isna(mwbe_status) or mwbe_status == "":

        add_issue(
            submission_id,
            "MWBE Validation",
            "REVIEW",
            "Medium",
            "MWBE status is missing"
        )


# ---------------------------------------------------------
# Review-aging validation
# ---------------------------------------------------------

for _, row in df.iterrows():

    submission_id = row["submission_id"]
    review_days = row["review_days"]

    if pd.notna(review_days):

        if review_days > 90:

            add_issue(
                submission_id,
                "Review Aging",
                "ESCALATE",
                "High",
                f"Submission has been in review for {int(review_days)} days"
            )

        elif review_days > 60:

            add_issue(
                submission_id,
                "Review Aging",
                "REVIEW",
                "Medium",
                f"Submission has been in review for {int(review_days)} days"
            )


# ---------------------------------------------------------
# Determine overall submission status
# ---------------------------------------------------------

all_submission_ids = df["submission_id"].dropna().unique()

overall_status = []

for submission_id in all_submission_ids:

    issues = [
        r for r in validation_records
        if r["submission_id"] == submission_id
    ]

    if not issues:

        status = "PASS"

    elif any(
        r["result"] == "ESCALATE"
        for r in issues
    ):

        status = "ESCALATE"

    elif any(
        r["severity"] == "High"
        for r in issues
    ):

        status = "ESCALATE"

    else:

        status = "REVIEW"

    overall_status.append({
        "submission_id": submission_id,
        "overall_status": status,
        "issue_count": len(issues),
    })


# ---------------------------------------------------------
# Save detailed validation results
# ---------------------------------------------------------

validation_df = pd.DataFrame(
    validation_records
)

if validation_df.empty:

    validation_df = pd.DataFrame(
        columns=[
            "submission_id",
            "check",
            "result",
            "severity",
            "message",
        ]
    )

validation_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Save summary
# ---------------------------------------------------------

overall_df = pd.DataFrame(overall_status)

summary_lines = [
    "CivicProcure Validation Summary",
    "=" * 35,
    "",
    f"Total submissions reviewed: {len(df)}",
    f"PASS: {(overall_df['overall_status'] == 'PASS').sum()}",
    f"REVIEW: {(overall_df['overall_status'] == 'REVIEW').sum()}",
    f"ESCALATE: {(overall_df['overall_status'] == 'ESCALATE').sum()}",
    "",
    f"Total validation issues: {len(validation_df)}",
]

if not validation_df.empty:

    summary_lines.extend([
        "",
        "Issues by check:",
    ])

    issue_counts = (
        validation_df["check"]
        .value_counts()
    )

    for check, count in issue_counts.items():

        summary_lines.append(
            f"- {check}: {count}"
        )

    summary_lines.extend([
        "",
        "Issues by severity:",
    ])

    severity_counts = (
        validation_df["severity"]
        .value_counts()
    )

    for severity, count in severity_counts.items():

        summary_lines.append(
            f"- {severity}: {count}"
        )


with open(
    SUMMARY_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(summary_lines)
    )


print("\n".join(summary_lines))
print("")
print(f"Detailed results: {OUTPUT_FILE}")
print(f"Summary: {SUMMARY_FILE}")