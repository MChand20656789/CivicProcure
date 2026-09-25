import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

agencies = [
    "Department of Education",
    "Department of Health",
    "Department of Transportation",
    "Department of Housing",
    "Department of Parks",
]

procurement_types = [
    "Goods",
    "Professional Services",
    "Human Services",
    "Construction",
    "Technology",
]

statuses = [
    "Approved",
    "Pending",
    "Under Review",
    "Rejected",
]

review_stages = [
    "Intake",
    "Financial Review",
    "Compliance Review",
    "Legal Review",
    "Final Approval",
]

mwbe_statuses = [
    "Yes",
    "No",
]

issue_types = [
    "",
    "Missing Documentation",
    "Vendor Information",
    "Financial Review",
    "Date Error",
    "Duplicate Submission",
]

vendors = [f"V{i:03d}" for i in range(1, 11)]

start_date = date(2026, 1, 1)

rows = []

for i in range(1, 61):

    submission_date = start_date + timedelta(
        days=random.randint(0, 240)
    )

    requested_amount = random.randint(10000, 500000)

    approved_amount = requested_amount * random.uniform(
        0.75, 1.00
    )

    contract_start = submission_date + timedelta(
        days=random.randint(15, 60)
    )

    contract_end = contract_start + timedelta(
        days=random.randint(180, 730)
    )

    status = random.choice(statuses)

    if status == "Approved":
        review_days = random.randint(5, 30)
    elif status == "Rejected":
        review_days = random.randint(5, 25)
    else:
        review_days = random.randint(15, 75)

    rows.append({
        "submission_id": f"S{i:04d}",
        "agency": random.choice(agencies),
        "vendor_id": random.choice(vendors),
        "procurement_type": random.choice(procurement_types),
        "submission_date": submission_date.isoformat(),
        "requested_amount": round(requested_amount, 2),
        "approved_amount": round(approved_amount, 2),
        "contract_start_date": contract_start.isoformat(),
        "contract_end_date": contract_end.isoformat(),
        "mwbe_status": random.choice(mwbe_statuses),
        "status": status,
        "review_stage": random.choice(review_stages),
        "compliance_status": "Compliant",
        "review_days": review_days,
        "issue_type": random.choice(issue_types),
    })


# ---------------------------------------------------------
# Introduce deliberate data-quality problems
# ---------------------------------------------------------

# 1. Missing vendor ID
rows[4]["vendor_id"] = ""

# 2. Missing MWBE information
rows[11]["mwbe_status"] = ""

# 3. Invalid contract dates
rows[18]["contract_end_date"] = rows[18]["contract_start_date"]

# 4. Requested amount exceeds approved amount by design
rows[25]["approved_amount"] = rows[25]["requested_amount"] - 5000

# 5. Invalid status
rows[32]["status"] = "Waiting"

# 6. Missing documentation
rows[37]["issue_type"] = "Missing Documentation"

# 7. Stuck submission
rows[42]["status"] = "Pending"
rows[42]["review_days"] = 120

# 8. Duplicate submission
duplicate = rows[15].copy()
rows.append(duplicate)


# ---------------------------------------------------------
# Write submissions
# ---------------------------------------------------------

submission_file = DATA_DIR / "procurement_submissions.csv"

with open(
    submission_file,
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)


# ---------------------------------------------------------
# Create contracts
# ---------------------------------------------------------

contract_rows = []

for row in rows[:60]:

    contract_rows.append({
        "contract_id": f"C{row['submission_id'][1:]}",
        "submission_id": row["submission_id"],
        "vendor_id": row["vendor_id"],
        "contract_start_date": row["contract_start_date"],
        "contract_end_date": row["contract_end_date"],
        "contract_value": row["approved_amount"],
        "contract_status": (
            "Active"
            if row["status"] == "Approved"
            else "Pending"
        ),
    })


contract_file = DATA_DIR / "contracts.csv"

with open(
    contract_file,
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=contract_rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(contract_rows)


print("Created procurement_submissions.csv")
print("Created contracts.csv")
print(f"Submission records: {len(rows)}")