# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cybersecurity Audit Decision App", page_icon="🛡️", layout="wide")

st.title("🛡️ General Cybersecurity Audit Decision-Support App")
st.caption("Assess risks, compliance gaps, vulnerabilities, and generate audit decisions.")

st.warning("Use only for authorized internal cybersecurity assessment and training.")



def audit_decision(risk, compliance_gap, critical_vulns):
    if critical_vulns >= 1 or risk == "Critical":
        return "Immediate Executive Action Required"
    elif risk == "High" or compliance_gap >= 3:
        return "Prioritize Remediation Within 30 Days"
    elif risk == "Medium":
        return "Monitor and Improve Controls"
    return "Acceptable with Routine Monitoring"

# -----------------------------
# 1. Asset Scope
# -----------------------------
st.header("1. Define Audit Scope")

assets = pd.DataFrame({
    "Asset": [
        "Customer Database",
        "Payment System",
        "Website / Portal",
        "Email System",
        "Cloud Storage",
        "Employee Portal"
    ],
    "Asset Type": [
        "Data", "Financial System", "Application", "Communication", "Cloud", "Internal System"
    ],
    "Data Sensitivity": [
        "High", "High", "Medium", "High", "High", "Medium"
    ],
    "Internet Exposed": [
        "No", "Yes", "Yes", "Yes", "No", "No"
    ],
    "Business Criticality": [
        "Critical", "Critical", "High", "High", "High", "Medium"
    ]
})

assets = st.data_editor(assets, use_container_width=True, num_rows="dynamic")

# -----------------------------
# 2. Threat and Risk Assessment
# -----------------------------
st.header("2. Threat and Risk Assessment")

risks = pd.DataFrame({
    "Risk Description": [
        "Unauthorized access to sensitive data",
        "Ransomware attack on critical systems",
        "Phishing attack against employees",
        "Cloud misconfiguration",
        "Third-party vendor breach",
        "Insider misuse of privileges"
    ],
    "Likelihood": [5, 4, 5, 4, 3, 3],
    "Impact": [5, 5, 4, 4, 4, 4],
    "Owner": [
        "CISO / Legal",
        "IT Operations",
        "Security Team / HR",
        "Cloud Admin",
        "Procurement / Risk",
        "HR / Security"
    ]
})

risks["Risk Score"] = risks["Likelihood"] * risks["Impact"]
risks["Risk Level"] = risks["Risk Score"].apply(risk_level)

risks = st.data_editor(risks, use_container_width=True, num_rows="dynamic")

fig = px.bar(
    risks.sort_values("Risk Score", ascending=False),
    x="Risk Description",
    y="Risk Score",
    color="Risk Level",
    title="Cybersecurity Risk Ranking"
)
st.plotly_chart(fig, use_container_width=True)

highest_risk = risks.sort_values("Risk Score", ascending=False).iloc[0]

# -----------------------------
# 3. Compliance Review
# -----------------------------
st.header("3. Compliance Review")

compliance = pd.DataFrame({
    "Control Area": [
        "Access Control",
        "MFA",
        "Data Encryption",
        "Backup and Recovery",
        "Incident Response",
        "Vendor Risk Management",
        "Security Awareness",
        "Log Monitoring"
    ],
    "Status": [
        "Partial",
        "Partial",
        "Implemented",
        "Implemented",
        "Partial",
        "Not Implemented",
        "Partial",
        "Partial"
    ],
    "Framework Mapping": [
        "ISO 27001 / NIST",
        "ISO 27001 / NIST",
        "ISO 27001 / GDPR",
        "NIST / ISO 27001",
        "NIST / ISO 27001",
        "ISO 27001",
        "ISO 27001",
        "NIST"
    ]
})

compliance = st.data_editor(compliance, use_container_width=True, num_rows="dynamic")

gap_count = compliance[compliance["Status"] != "Implemented"].shape[0]

st.metric("Open Compliance Gaps", gap_count)

# -----------------------------
# 4. Vulnerability Findings
# -----------------------------
st.header("4. Vulnerability Findings")

vulns = pd.DataFrame({
    "Finding": [
        "Unpatched public-facing server",
        "Weak password policy",
        "Overly permissive firewall rule",
        "No formal vendor security review"
    ],
    "Severity": [
        "Critical",
        "High",
        "High",
        "Medium"
    ],
    "Recommended Action": [
        "Patch immediately and verify configuration",
        "Enforce MFA and password policy",
        "Apply least privilege firewall rules",
        "Create vendor security assessment process"
    ],
    "Target Time": [
        "72 hours",
        "30 days",
        "14 days",
        "60 days"
    ]
})

vulns = st.data_editor(vulns, use_container_width=True, num_rows="dynamic")

critical_vulns = vulns[vulns["Severity"] == "Critical"].shape[0]

st.metric("Critical Vulnerabilities", critical_vulns)

# -----------------------------
# 5. Decision Engine
# -----------------------------
st.header("5. Audit Decision Engine")

final_decision = audit_decision(
    highest_risk["Risk Level"],
    gap_count,
    critical_vulns
)

if "Immediate" in final_decision:
    st.error(f"Decision: {final_decision}")
elif "Prioritize" in final_decision:
    st.warning(f"Decision: {final_decision}")
else:
    st.success(f"Decision: {final_decision}")

st.subheader("Decision Basis")

decision_table = pd.DataFrame({
    "Decision Factor": [
        "Highest Risk",
        "Highest Risk Level",
        "Highest Risk Score",
        "Open Compliance Gaps",
        "Critical Vulnerabilities"
    ],
    "Value": [
        highest_risk["Risk Description"],
        highest_risk["Risk Level"],
        highest_risk["Risk Score"],
        gap_count,
        critical_vulns
    ]
})

st.table(decision_table)

# -----------------------------
# 6. Recommendations
# -----------------------------
st.header("6. Recommended Action Plan")

recommendations = pd.DataFrame({
    "Priority": [
        "Immediate",
        "Immediate",
        "Short-Term",
        "Short-Term",
        "Long-Term"
    ],
    "Recommendation": [
        "Remediate all critical vulnerabilities",
        "Strengthen access control and MFA",
        "Update incident response playbooks",
        "Conduct employee phishing awareness training",
        "Adopt continuous monitoring and zero-trust principles"
    ],
    "Expected Impact": [
        "Reduce immediate exposure",
        "Reduce unauthorized access risk",
        "Improve breach containment",
        "Reduce human error",
        "Improve long-term cyber resilience"
    ]
})

st.dataframe(recommendations, use_container_width=True)

# -----------------------------
# 7. KPIs
# -----------------------------
st.header("7. Cybersecurity Audit KPIs")

kpis = pd.DataFrame({
    "KPI": [
        "Patch Compliance Rate %",
        "MFA Coverage %",
        "Mean Time to Detect - MTTD",
        "Mean Time to Respond - MTTR",
        "Training Completion %",
        "Open Critical Findings"
    ],
    "Current": [78, 65, 8, 24, 70, critical_vulns],
    "Target": [95, 100, 4, 12, 90, 0]
})

st.dataframe(kpis, use_container_width=True)

fig_kpi = px.bar(
    kpis,
    x="KPI",
    y=["Current", "Target"],
    barmode="group",
    title="Current vs Target Cybersecurity KPIs"
)

st.plotly_chart(fig_kpi, use_container_width=True)

# -----------------------------
# 8. Export Report
# -----------------------------
st.header("8. Export Audit Decision Report")

report = f"""
GENERAL CYBERSECURITY AUDIT DECISION REPORT

Highest Risk:
{highest_risk["Risk Description"]}

Risk Level:
{highest_risk["Risk Level"]}

Risk Score:
{highest_risk["Risk Score"]}

Open Compliance Gaps:
{gap_count}

Critical Vulnerabilities:
{critical_vulns}

Final Audit Decision:
{final_decision}

Recommended Actions:
1. Remediate critical vulnerabilities.
2. Apply MFA and strengthen access control.
3. Improve incident response readiness.
4. Conduct employee awareness training.
5. Adopt continuous monitoring and zero-trust principles.
"""

st.download_button(
    "Download Audit Decision Report",
    report,
    file_name="cybersecurity_audit_decision_report.txt",
    mime="text/plain"
)