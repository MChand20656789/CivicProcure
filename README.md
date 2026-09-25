# CivicProcure

## Procurement Operations Analytics & Data Quality System

CivicProcure is a **simulated procurement operations analytics system** designed to demonstrate how data validation, workflow monitoring, stakeholder feedback, and reporting can support government procurement operations.

The project combines **Python, SQL, SQLite, Pandas, Plotly, and Streamlit** to create a reproducible workflow for ingesting procurement data, validating submissions, identifying issues requiring follow-up, calculating operational metrics, analyzing stakeholder feedback, and producing management-oriented reports and dashboards.

> **Important:** CivicProcure uses fictional/simulated procurement data. It does not use confidential government data and does not represent actual experience with any government procurement system.

---

## Project Objective

Procurement operations depend on accurate submissions, complete documentation, reliable vendor information, timely reviews, and clear reporting.

CivicProcure models a simplified workflow:

```text
Procurement Data
       ↓
Data Validation
       ↓
Completeness & Quality Checks
       ↓
Financial & Date Validation
       ↓
Vendor Validation
       ↓
Review Aging Analysis
       ↓
Operational Metrics
       ↓
Stakeholder Feedback Analysis
       ↓
Process Improvement
       ↓
SQL Reporting & Dashboard
```

The goal is to demonstrate practical skills in:

* Data analysis
* Data quality and validation
* Government operations analytics
* Procurement workflow analysis
* SQL reporting
* Business process analysis
* Stakeholder feedback analysis
* KPI development
* Dashboard development
* Process improvement
* Reproducible analytics workflows

---

## Key Features

### 1. Procurement Data Generation

Creates a controlled fictional dataset containing:

* Procurement submissions
* Vendors
* Contracts
* Stakeholder feedback

The dataset intentionally contains data-quality issues so that the validation system can identify them.

Examples include:

* Duplicate submissions
* Missing vendor information
* Missing MWBE information
* Missing documentation
* Invalid contract dates
* Invalid statuses
* Aging submissions
* Incomplete records

---

### 2. Automated Validation

The validation engine evaluates procurement submissions using multiple checks.

Validation categories include:

* Required-field completeness
* Vendor validation
* Duplicate detection
* Date validation
* Financial validation
* Status validation
* MWBE validation
* Review aging

Each submission receives an operational outcome:

```text
PASS
REVIEW
ESCALATE
```

The validation process produces both record-level results and an overall quality summary.

---

### 3. Procurement Metrics

The metrics pipeline calculates operational KPIs including:

* Total submissions
* Pending submissions
* Approved submissions
* Rejected submissions
* Average review time
* Requested amount
* Approved amount
* Approval rate
* Follow-up count
* High-severity issues
* Compliance/data-quality issues

Additional metrics are calculated by:

* Agency
* Review stage
* Issue category
* Procurement type

---

### 4. SQLite Database

CivicProcure loads the processed datasets into a relational SQLite database.

Database tables include:

```text
procurement_submissions
vendors
contracts
stakeholder_feedback
validation_results
```

This allows operational questions to be answered using SQL rather than relying exclusively on Python transformations.

---

### 5. SQL Reporting

The project includes SQL queries for common procurement-operations questions, including:

* Procurement volume by agency
* Average review time by agency
* Pending submissions
* Aging submissions
* Requested vs. approved amounts
* Procurement volume by type
* Issues by category
* Vendors with the most submissions
* Review workload by stage
* Stakeholder issues by category
* Open stakeholder issues
* Proposed improvements based on stakeholder feedback

---

### 6. Stakeholder Feedback Analysis

The stakeholder feedback dataset simulates feedback from agency users.

The analysis identifies recurring operational problems such as:

| Issue                 | Proposed Process Improvement            |
| --------------------- | --------------------------------------- |
| Missing Documentation | Pre-submission completeness checks      |
| Vendor Information    | Required-field validation               |
| Review Aging          | Aging metrics and escalation monitoring |
| Financial Data        | Automated amount validation             |
| Duplicate Submission  | Duplicate detection                     |
| User Experience       | Clearer status reporting                |
| Documentation         | Standardized job aids                   |
| Reporting Visibility  | Recurring KPI dashboard                 |

The project connects stakeholder feedback to specific process-improvement opportunities rather than treating feedback as an isolated dataset.

---

## Dashboard

The Streamlit dashboard provides an operational view of procurement activity and data quality.

Dashboard components include:

* Procurement KPIs
* Agency-level metrics
* Review-stage workload
* Issue categories
* Requested vs. approved amounts
* Aging submissions
* Follow-up records
* Stakeholder/process-improvement information

The dashboard is designed around the types of questions an operations or analytics team might ask when monitoring procurement workflows.

---

## Project Structure

```text
CivicProcure/
│
├── data/
│   ├── procurement_submissions.csv
│   ├── vendors.csv
│   ├── contracts.csv
│   └── stakeholder_feedback.csv
│
├── scripts/
│   ├── create_data.py
│   ├── validate_submissions.py
│   ├── calculate_metrics.py
│   ├── load_database.py
│   ├── analyze_feedback.py
│   └── generate_report.py
│
├── sql/
│   └── procurement_queries.sql
│
├── dashboard/
│   └── app.py
│
├── output/
│   ├── cleaned reports and metrics
│   ├── validation results
│   └── generated analysis files
│
├── README.md
├── requirements.txt
├── setup.sh
└── .gitignore
```

The SQLite database is generated locally and excluded from version control.

---

## Technologies

### Programming & Analysis

* Python
* Pandas
* NumPy

### Database & SQL

* SQLite
* SQL
* Relational data modeling

### Visualization

* Plotly
* Streamlit

### Data Engineering

* ETL workflows
* Data validation
* Data cleaning
* Duplicate detection
* Data-quality reporting
* Automated metric generation

### Analytics

* KPI development
* Operational reporting
* Workflow analysis
* Review-aging analysis
* Stakeholder feedback analysis
* Process improvement

---

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd CivicProcure
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

This project intentionally avoids PyArrow.

Because Streamlit normally declares PyArrow as a dependency, the project uses `setup.sh` to install Streamlit without automatically installing PyArrow.

Run:

```bash
./setup.sh
```

### 4. Generate the simulated data

```bash
python scripts/create_data.py
```

### 5. Run validation

```bash
python scripts/validate_submissions.py
```

### 6. Calculate metrics

```bash
python scripts/calculate_metrics.py
```

### 7. Load the SQLite database

```bash
python scripts/load_database.py
```

### 8. Run SQL reports

```bash
sqlite3 -header -column output/civicprocure.db < sql/procurement_queries.sql > output/sql_results.txt
```

### 9. Analyze stakeholder feedback

```bash
python scripts/analyze_feedback.py
```

### 10. Generate reports

```bash
python scripts/generate_report.py
```

### 11. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

---

## Example Validation Results

The simulated dataset contains 61 procurement submissions, including deliberately introduced data-quality issues.

Example validation output:

```text
Total submissions reviewed: 61

PASS: 44
REVIEW: 12
ESCALATE: 4

Total validation issues: 18

Issues by check:
- Review Aging: 11
- Duplicate Detection: 2
- Completeness: 1
- Vendor Validation: 1
- Date Validation: 1
- Status Validation: 1
- MWBE Validation: 1

Issues by severity:
- Medium: 12
- High: 6
```

These figures describe the fictional dataset created by the project and should not be interpreted as real procurement statistics.

---

## Example Business Questions

CivicProcure can answer questions such as:

**Operational performance**

* Which agencies have the highest procurement volume?
* Which agencies have longer average review times?
* Where is review workload concentrated?

**Data quality**

* What types of validation problems occur most frequently?
* Which submissions require follow-up?
* Which issues have high severity?

**Workflow**

* Which review stages have the largest workload?
* Which submissions are aging?
* Where might manual review be creating bottlenecks?

**Stakeholder experience**

* What problems are agency users reporting?
* Which issues occur repeatedly?
* What process improvements could address recurring problems?

---

## Process Improvement Framework

CivicProcure connects operational data and stakeholder feedback through a simple improvement framework:

```text
Observed Problem
       ↓
Identify Bottleneck
       ↓
Determine Root Cause
       ↓
Propose Process Change
       ↓
Define Expected Effect
       ↓
Monitor KPI
```

For example:

```text
Problem:
Incomplete procurement submissions

        ↓

Bottleneck:
Manual identification of missing information

        ↓

Process Change:
Pre-submission completeness validation

        ↓

Expected Effect:
Fewer incomplete submissions reaching manual review
```

---

## Data Quality Philosophy

The project treats data validation as an operational process rather than simply a preprocessing step.

Validation results are preserved and analyzed so that users can distinguish between:

* Clean records
* Records requiring review
* Records requiring escalation

This makes the pipeline useful for both **data-quality monitoring** and **operational decision support**.

---

## Limitations

CivicProcure is intentionally a small portfolio project.

It does not attempt to reproduce a real government procurement platform.

The project does not claim:

* Actual government procurement experience
* Experience with PASSPort
* Experience with HHS Accelerator
* Access to confidential procurement records
* Government compliance certification
* Actual M/WBE program administration

Instead, the project demonstrates transferable analytical and operational skills using a controlled fictional environment.

---

## Future Improvements

Potential future enhancements include:

* Power BI version of the dashboard
* Automated scheduled reporting
* More sophisticated anomaly detection
* Role-based dashboard views
* Additional workflow metrics
* Automated stakeholder issue prioritization
* Unit tests for validation rules
* Data-quality regression tests
* Logging and pipeline monitoring
* Configuration-driven validation rules
* Automated report generation

---

## Portfolio Relevance

CivicProcure demonstrates the intersection of:

**Data Analysis + Government Operations + Process Improvement + Stakeholder Experience**

The project is particularly useful for demonstrating how an analyst can move from raw operational data to:

```text
Data
 ↓
Validation
 ↓
Analysis
 ↓
Reporting
 ↓
Stakeholder Insight
 ↓
Process Improvement
```

The emphasis is on **accuracy, reproducibility, operational reporting, and actionable analysis** rather than building an unnecessarily complex machine-learning model.
