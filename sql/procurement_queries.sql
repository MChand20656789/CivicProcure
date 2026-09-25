-- =========================================================
-- CivicProcure SQL Reporting
-- =========================================================


-- ---------------------------------------------------------
-- 1. Procurement volume by agency
-- ---------------------------------------------------------

SELECT
    agency,
    COUNT(*) AS submission_count
FROM procurement_submissions
GROUP BY agency
ORDER BY submission_count DESC;


-- ---------------------------------------------------------
-- 2. Average review time by agency
-- ---------------------------------------------------------

SELECT
    agency,
    ROUND(AVG(review_days), 2) AS avg_review_days
FROM procurement_submissions
GROUP BY agency
ORDER BY avg_review_days DESC;


-- ---------------------------------------------------------
-- 3. Pending submissions
-- ---------------------------------------------------------

SELECT
    submission_id,
    agency,
    vendor_id,
    procurement_type,
    status,
    review_stage,
    review_days
FROM procurement_submissions
WHERE status IN ('Pending', 'Under Review')
ORDER BY review_days DESC;


-- ---------------------------------------------------------
-- 4. Aging submissions
-- ---------------------------------------------------------

SELECT
    submission_id,
    agency,
    status,
    review_stage,
    review_days
FROM procurement_submissions
WHERE review_days > 60
ORDER BY review_days DESC;


-- ---------------------------------------------------------
-- 5. Requested vs approved amounts
-- ---------------------------------------------------------

SELECT
    agency,
    ROUND(SUM(requested_amount), 2)
        AS total_requested,
    ROUND(SUM(approved_amount), 2)
        AS total_approved,
    ROUND(
        SUM(requested_amount)
        - SUM(approved_amount),
        2
    ) AS amount_difference
FROM procurement_submissions
GROUP BY agency
ORDER BY total_requested DESC;


-- ---------------------------------------------------------
-- 6. Procurement volume by type
-- ---------------------------------------------------------

SELECT
    procurement_type,
    COUNT(*) AS submission_count,
    ROUND(SUM(requested_amount), 2)
        AS requested_amount
FROM procurement_submissions
GROUP BY procurement_type
ORDER BY requested_amount DESC;


-- ---------------------------------------------------------
-- 7. Issues by category
-- ---------------------------------------------------------

SELECT
    "check",
    severity,
    COUNT(*) AS issue_count
FROM validation_results
GROUP BY
    "check",
    severity
ORDER BY issue_count DESC;


-- ---------------------------------------------------------
-- 8. Vendors with the most submissions
-- ---------------------------------------------------------

SELECT
    v.vendor_id,
    v.vendor_name,
    COUNT(p.submission_id)
        AS submission_count
FROM vendors v
LEFT JOIN procurement_submissions p
    ON v.vendor_id = p.vendor_id
GROUP BY
    v.vendor_id,
    v.vendor_name
ORDER BY submission_count DESC;


-- ---------------------------------------------------------
-- 9. Review workload by stage
-- ---------------------------------------------------------

SELECT
    review_stage,
    COUNT(*) AS submission_count,
    ROUND(AVG(review_days), 2)
        AS avg_review_days,
    MAX(review_days)
        AS max_review_days
FROM procurement_submissions
GROUP BY review_stage
ORDER BY avg_review_days DESC;


-- ---------------------------------------------------------
-- 10. Stakeholder issues by category
-- ---------------------------------------------------------

SELECT
    issue_category,
    severity,
    COUNT(*) AS feedback_count
FROM stakeholder_feedback
GROUP BY
    issue_category,
    severity
ORDER BY feedback_count DESC;


-- ---------------------------------------------------------
-- 11. Open stakeholder issues
-- ---------------------------------------------------------

SELECT
    agency,
    stakeholder_role,
    system_area,
    issue_category,
    severity,
    requested_improvement,
    status
FROM stakeholder_feedback
WHERE status != 'Closed'
ORDER BY
    CASE severity
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
        ELSE 4
    END;


-- ---------------------------------------------------------
-- 12. Stakeholder feedback → proposed improvement
-- ---------------------------------------------------------

SELECT
    issue_category,
    COUNT(*) AS feedback_count,
    GROUP_CONCAT(
        DISTINCT requested_improvement
    ) AS proposed_improvements
FROM stakeholder_feedback
GROUP BY issue_category
ORDER BY feedback_count DESC;