import streamlit as st
import pandas as pd
from model import predict_recovery, recommend_action
from recovery import execute_recovery

st.set_page_config(
    page_title="RecoverAI",
    page_icon="💳",
    layout="wide"
)

st.title("🤖 RecoverAI")
st.subheader("Intelligent Payment Recovery Agent")

st.write(
    "RecoverAI analyzes failed payments, predicts recovery probability, "
    "and recommends a bounded recovery action."
)

data = pd.read_csv("payments.csv")

results = []

for _, payment in data.iterrows():

    probability = predict_recovery(payment)

    action = recommend_action(
        payment,
        probability
    )

    result = execute_recovery(
        payment,
        probability,
        action
    )

    results.append(result)

results_df = pd.DataFrame(results)

st.header("📊 Recovery Overview")

total_risk = results_df["amount"].sum()
recovered = results_df["recovered_amount"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Payments Analyzed",
        len(results_df)
    )

with col2:
    st.metric(
        "Revenue at Risk",
        f"₹{total_risk:,.0f}"
    )

with col3:
    st.metric(
        "Recovered Revenue",
        f"₹{recovered:,.0f}"
    )

st.header("🔍 Recovery Decisions")

st.dataframe(
    results_df,
    use_container_width=True
)

st.header("🧠 Agent Workflow")

st.write("""
**1. Detect** → Identify failed payments

**2. Predict** → Estimate recovery probability

**3. Decide** → Select the best recovery action

**4. Execute** → Run a bounded recovery workflow

**5. Measure** → Track recovered revenue and maintain an audit trail
""")

st.info(
    "Demo environment: all recovery actions are simulated. "
    "No real payments are processed."
)
st.header("💰 Recovery Performance")

recovery_rate = (
    recovered / total_risk * 100
    if total_risk > 0
    else 0
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Recovery Rate",
        f"{recovery_rate:.1f}%"
    )

with col2:
    st.metric(
        "Unrecovered Revenue",
        f"₹{total_risk - recovered:,.0f}"
    )
    st.header("📋 Agent Audit Trail")

audit_columns = [
    "payment_id",
    "probability",
    "action",
    "status",
    "recovered_amount",
    "timestamp"
]

st.dataframe(
    results_df[audit_columns],
    use_container_width=True
)

st.caption(
    "Every recovery decision is recorded with its probability, "
    "selected action, outcome, and timestamp."
)