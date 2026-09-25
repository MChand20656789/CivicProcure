import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE = DATA_DIR / "stakeholder_feedback.csv"

ISSUE_SUMMARY_FILE = (
    OUTPUT_DIR / "stakeholder_issue_summary.csv"
)

AGENCY_SUMMARY_FILE = (
    OUTPUT_DIR / "stakeholder_agency_summary.csv"
)

IMPROVEMENT_FILE = (
    OUTPUT_DIR / "process_improvement_report.md"
)


# ---------------------------------------------------------
# Load feedback
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Issue-category analysis
# ---------------------------------------------------------

issue_summary = (
    df.groupby(
        ["issue_category", "severity"]
    )
    .agg(
        feedback_count=("feedback_id", "count")
    )
    .reset_index()
    .sort_values(
        ["feedback_count", "severity"],
        ascending=[False, True]
    )
)

issue_summary.to_csv(
    ISSUE_SUMMARY_FILE,
    index=False
)


# ---------------------------------------------------------
# Agency-level analysis
# ---------------------------------------------------------

agency_summary = (
    df.groupby("agency")
    .agg(
        feedback_count=("feedback_id", "count"),
        high_severity_issues=(
            "severity",
            lambda x: (x == "High").sum()
        ),
        open_issues=(
            "status",
            lambda x: (x != "Closed").sum()
        ),
    )
    .reset_index()
    .sort_values(
        "feedback_count",
        ascending=False
    )
)

agency_summary.to_csv(
    AGENCY_SUMMARY_FILE,
    index=False
)


# ---------------------------------------------------------
# Requested-improvement analysis
# ---------------------------------------------------------

improvement_counts = (
    df.groupby("requested_improvement")
    .size()
    .reset_index(
        name="request_count"
    )
    .sort_values(
        "request_count",
        ascending=False
    )
)


# ---------------------------------------------------------
# Process-improvement mappings
# ---------------------------------------------------------

improvement_map = {
    "Missing Documentation": {
        "bottleneck": (
            "Incomplete documentation is discovered "
            "during manual review."
        ),
        "proposed_change": (
            "Introduce pre-submission completeness "
            "validation and a standardized checklist."
        ),
        "expected_effect": (
            "Reduce incomplete submissions reaching "
            "manual review and reduce repeated clarification."
        ),
    },

    "Vendor Information": {
        "bottleneck": (
            "Required vendor information may be "
            "missing during intake."
        ),
        "proposed_change": (
            "Add required-field validation against "
            "the vendor master."
        ),
        "expected_effect": (
            "Reduce intake errors and improve "
            "vendor-data consistency."
        ),
    },

    "Review Aging": {
        "bottleneck": (
            "Older submissions can remain in review "
            "without clear escalation visibility."
        ),
        "proposed_change": (
            "Create review-aging metrics and "
            "escalation alerts."
        ),
        "expected_effect": (
            "Improve visibility into delayed submissions "
            "and support earlier intervention."
        ),
    },

    "Financial Data": {
        "bottleneck": (
            "Financial discrepancies may be discovered "
            "late in the review process."
        ),
        "proposed_change": (
            "Add automated requested-versus-approved "
            "amount validation."
        ),
        "expected_effect": (
            "Identify financial discrepancies earlier "
            "and reduce manual rework."
        ),
    },

    "Duplicate Submission": {
        "bottleneck": (
            "Duplicate submissions can create "
            "unnecessary review work."
        ),
        "proposed_change": (
            "Add automated duplicate detection "
            "using submission identifiers and key fields."
        ),
        "expected_effect": (
            "Reduce redundant review activity."
        ),
    },

    "User Experience": {
        "bottleneck": (
            "Stakeholders may have difficulty locating "
            "submission status information."
        ),
        "proposed_change": (
            "Create a clearer status summary and "
            "standardized reporting view."
        ),
        "expected_effect": (
            "Improve status visibility and reduce "
            "repeated support questions."
        ),
    },

    "Documentation": {
        "bottleneck": (
            "Stakeholders repeatedly ask which "
            "documents are required."
        ),
        "proposed_change": (
            "Create standardized job aids and "
            "submission guidance."
        ),
        "expected_effect": (
            "Improve user adoption and reduce "
            "repeated procedural questions."
        ),
    },

    "Reporting Visibility": {
        "bottleneck": (
            "Stakeholders lack a simple operational "
            "view of procurement activity."
        ),
        "proposed_change": (
            "Create a recurring KPI dashboard covering "
            "volume, aging, status, and financial metrics."
        ),
        "expected_effect": (
            "Improve management visibility and "
            "support data-driven decisions."
        ),
    },
}


# ---------------------------------------------------------
# Build process-improvement report
# ---------------------------------------------------------

report_lines = [
    "# CivicProcure Process Improvement Analysis",
    "",
    "> Simulated analysis using fictional procurement "
    "operations and stakeholder feedback data.",
    "",
    "## Summary",
    "",
    (
        f"The simulated dataset contains "
        f"{len(df)} stakeholder feedback records "
        "covering procurement intake, vendor management, "
        "review workflow, financial review, reporting, "
        "and system usability."
    ),
    "",
    "## Stakeholder Findings",
    "",
]


for _, row in issue_summary.iterrows():

    category = row["issue_category"]
    severity = row["severity"]
    count = row["feedback_count"]

    report_lines.extend([
        f"### {category}",
        "",
        f"- Feedback records: **{count}**",
        f"- Severity represented: **{severity}**",
    ])

    if category in improvement_map:

        mapping = improvement_map[category]

        report_lines.extend([
            "",
            f"**Bottleneck:** "
            f"{mapping['bottleneck']}",
            "",
            f"**Proposed improvement:** "
            f"{mapping['proposed_change']}",
            "",
            f"**Expected effect:** "
            f"{mapping['expected_effect']}",
        ])

    report_lines.append("")


# ---------------------------------------------------------
# Requested improvements
# ---------------------------------------------------------

report_lines.extend([
    "## Most Requested Improvements",
    "",
])

for _, row in improvement_counts.iterrows():

    report_lines.append(
        f"- {row['requested_improvement']} "
        f"({row['request_count']} requests)"
    )


# ---------------------------------------------------------
# Agency findings
# ---------------------------------------------------------

report_lines.extend([
    "",
    "## Agency-Level Feedback",
    "",
    "| Agency | Feedback | High Severity | Open |",
    "|---|---:|---:|---:|",
])

for _, row in agency_summary.iterrows():

    report_lines.append(
        f"| {row['agency']} | "
        f"{row['feedback_count']} | "
        f"{row['high_severity_issues']} | "
        f"{row['open_issues']} |"
    )


# ---------------------------------------------------------
# Process-improvement framework
# ---------------------------------------------------------

report_lines.extend([
    "",
    "## Process Improvement Framework",
    "",
    "| Problem | Evidence | Proposed Change | Expected Effect |",
    "|---|---|---|---|",
])

for category, mapping in improvement_map.items():

    matching = df[
        df["issue_category"] == category
    ]

    if len(matching) == 0:
        continue

    evidence = (
        f"{len(matching)} stakeholder "
        f"feedback record(s)"
    )

    report_lines.append(
        f"| {category} | "
        f"{evidence} | "
        f"{mapping['proposed_change']} | "
        f"{mapping['expected_effect']} |"
    )


# ---------------------------------------------------------
# Write report
# ---------------------------------------------------------

with open(
    IMPROVEMENT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(report_lines)
    )


# ---------------------------------------------------------
# Console output
# ---------------------------------------------------------

print()
print("CivicProcure Stakeholder Analysis")
print("=" * 40)

print(
    f"Feedback records analyzed: {len(df)}"
)

print()
print("Top issue categories:")

for _, row in issue_summary.head(5).iterrows():

    print(
        f"- {row['issue_category']}: "
        f"{row['feedback_count']}"
    )

print()
print("Output files:")
print(ISSUE_SUMMARY_FILE)
print(AGENCY_SUMMARY_FILE)
print(IMPROVEMENT_FILE)