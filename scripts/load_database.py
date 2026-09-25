import sqlite3
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DB_FILE = OUTPUT_DIR / "civicprocure.db"


# ---------------------------------------------------------
# Connect to SQLite
# ---------------------------------------------------------

connection = sqlite3.connect(DB_FILE)


# ---------------------------------------------------------
# Load CSV files
# ---------------------------------------------------------

submissions = pd.read_csv(
    DATA_DIR / "procurement_submissions.csv"
)

vendors = pd.read_csv(
    DATA_DIR / "vendors.csv"
)

contracts = pd.read_csv(
    DATA_DIR / "contracts.csv"
)

feedback = pd.read_csv(
    DATA_DIR / "stakeholder_feedback.csv"
)

validation = pd.read_csv(
    OUTPUT_DIR / "validation_results.csv"
)


# ---------------------------------------------------------
# Write tables
# ---------------------------------------------------------

submissions.to_sql(
    "procurement_submissions",
    connection,
    if_exists="replace",
    index=False,
)

vendors.to_sql(
    "vendors",
    connection,
    if_exists="replace",
    index=False,
)

contracts.to_sql(
    "contracts",
    connection,
    if_exists="replace",
    index=False,
)

feedback.to_sql(
    "stakeholder_feedback",
    connection,
    if_exists="replace",
    index=False,
)

validation.to_sql(
    "validation_results",
    connection,
    if_exists="replace",
    index=False,
)


# ---------------------------------------------------------
# Verify tables
# ---------------------------------------------------------

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
    """,
    connection,
)

print("CivicProcure SQLite Database")
print("=" * 35)

for table in tables["name"]:
    print(f"- {table}")

connection.close()

print()
print(f"Database created: {DB_FILE}")