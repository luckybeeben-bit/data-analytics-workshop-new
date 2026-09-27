import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Decision Page", layout="wide")
DATA_PATH = "day03/case03_branch/data/branch_customer_performance.csv"
df = pd.read_csv(DATA_PATH)

st.title("Executive Decision Page")
st.caption("Case 3 — Branch Investment Decision")

st.header("Decision Question")
st.write("Which three branches should receive improvement investment, and why?")

summary = (
    df.groupby("Branch", as_index=False)
      .agg(
          Revenue=("Revenue","sum"),
          Profit=("Profit","sum"),
          Orders=("Orders","sum"),
          Rating=("Rating","mean"),
          Repeat_Purchase_Rate=("Repeat_Purchase_Rate","mean"),
          Complaint_Rate=("Complaint_Rate","mean"),
          Service_Time_Min=("Service_Time_Min","mean")
      )
)

st.header("Executive KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"{summary['Revenue'].sum():,.0f}")
c2.metric("Total Profit", f"{summary['Profit'].sum():,.0f}")
c3.metric("Avg Rating", f"{summary['Rating'].mean():.2f}")
c4.metric("Avg Complaint Rate", f"{summary['Complaint_Rate'].mean():.1%}")

st.header("Evidence")
fig = px.scatter(
    summary,
    x="Service_Time_Min",
    y="Complaint_Rate",
    size="Revenue",
    hover_name="Branch",
    title="Service Time vs Complaint Rate"
)
st.plotly_chart(fig, width="stretch")

# TODO: add 1–3 decision-relevant charts
# TODO: write evidence-based insight headlines

st.header("Recommendation")
st.info("TODO: Write recommendation only after validating evidence.")

st.header("Action Plan")
action_plan = pd.DataFrame({
    "Action": ["TODO"],
    "Owner": ["TODO"],
    "Timeline": ["TODO"],
    "KPI": ["TODO"],
    "Target": ["TODO"],
    "Expected Impact": ["TODO"]
})
st.dataframe(action_plan, width="stretch")
