"""Completed LAB07 example. Prompts and reasoning: example_app_guide.md.

Run: streamlit run day03/app_starter/example_app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Executive Decision Page — Example", layout="wide")
DATA_PATH = Path(__file__).resolve().parents[1] / "case03_branch/data/branch_customer_performance.csv"
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

st.title("Executive Decision Page")
st.caption("Case 3 — Branch Investment Decision | ตัวอย่างเฉลย LAB07")
st.header("Decision Question")
st.write("ควรเลือกลงทุนปรับปรุง 3 สาขาใด และควรแก้ปัญหาอะไร?")

# Validate evidence before creating a recommendation; never silently drop bad rows.
numeric_columns = [
    "Revenue", "Profit", "Orders", "Rating", "Repeat_Purchase_Rate",
    "Complaint_Rate", "Service_Time_Min",
]
required_columns = ["Branch", *numeric_columns]
if not set(required_columns).issubset(df.columns):
    st.error("ข้อมูลขาดคอลัมน์ที่จำเป็น กรุณาตรวจ CSV ก่อนวิเคราะห์")
    st.stop()
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")
invalid_data = (
    df.empty
    or df[required_columns].isna().any().any()
    or df["Branch"].astype(str).str.strip().eq("").any()
    or df[numeric_columns].isin([float("inf"), float("-inf")]).any().any()
    or (df[["Revenue", "Orders", "Service_Time_Min"]] < 0).any().any()
    or not df["Rating"].between(0, 5).all()
    or not df["Repeat_Purchase_Rate"].between(0, 1).all()
    or not df["Complaint_Rate"].between(0, 1).all()
)
if invalid_data:
    st.error("พบข้อมูลว่างหรือค่าผิดช่วง (Rating ใช้สเกล 0–5 และอัตราใช้ 0–1) กรุณาตรวจ CSV")
    st.stop()
if df["Branch"].nunique() < 4 or df["Revenue"].sum() <= 0:
    st.error("ตัวอย่างนี้ต้องมีอย่างน้อย 4 สาขาเพื่อเปรียบเทียบ 3 สาขาที่เลือกกับสาขาอื่น และรายได้รวมต้องเป็นบวก")
    st.stop()

summary = (
    df.groupby("Branch", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Orders", "sum"),
        Rating=("Rating", "mean"),
        Repeat_Purchase_Rate=("Repeat_Purchase_Rate", "mean"),
        Complaint_Rate=("Complaint_Rate", "mean"),
        Service_Time_Min=("Service_Time_Min", "mean"),
        Rows=("Branch", "size"),
    )
)
# A transparent teaching rule: complaints first, service time only breaks ties.
ranking = summary.sort_values(
    ["Complaint_Rate", "Service_Time_Min", "Branch"],
    ascending=[False, False, True],
).reset_index(drop=True)
ranking.insert(0, "Priority", range(1, len(ranking) + 1))
selected = ranking.head(3).copy()
others = ranking.iloc[3:]
branch_names = ", ".join(selected["Branch"])
summary["Group"] = summary["Branch"].isin(selected["Branch"]).map(
    {True: "เสนอทดลองปรับปรุง", False: "สาขาอื่น"}
)
colors = {"เสนอทดลองปรับปรุง": "#c2410c", "สาขาอื่น": "#64748b"}
group_order = {"Group": list(colors)}

st.header("Executive KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"{summary['Revenue'].sum():,.0f}")
c2.metric("Total Profit", f"{summary['Profit'].sum():,.0f}")
c3.metric("Avg Rating (equal branch weight)", f"{summary['Rating'].mean():.2f}")
c4.metric("Avg Complaint Rate (equal branch weight)", f"{summary['Complaint_Rate'].mean():.1%}")
st.caption(
    "Revenue / Profit / Orders รวมด้วย sum; ตัวชี้วัดอื่นเฉลี่ยแต่ละแถวภายในสาขา "
    "แล้วเฉลี่ยแต่ละสาขาเท่ากันเมื่อเปรียบเทียบกลุ่ม ไม่ใช่อัตรารวมของลูกค้าทั้งบริษัท "
    "ยังไม่มีตัวหารจริงของแต่ละอัตรา จึงไม่ใช้ Orders ถ่วงน้ำหนักโดยอัตโนมัติ"
)

st.header("Evidence")
st.write(
    "เกณฑ์ตัวอย่าง: เรียง Complaint Rate จากสูงไปต่ำ → ถ้าเท่ากันใช้ Service Time "
    "จากสูงไปต่ำ → ถ้ายังเท่ากันเรียงชื่อสาขา แล้วเลือก 3 อันดับแรก "
    "เป็นเกณฑ์ที่ผู้วิเคราะห์กำหนดเพื่อจัดลำดับปัญหาบริการ ไม่ใช่แบบจำลองผลตอบแทนการลงทุน"
)
with st.expander("ตรวจตารางหลักฐานและลำดับสาขา"):
    st.dataframe(ranking, width="stretch", hide_index=True)

fig = px.scatter(
    summary, x="Service_Time_Min", y="Complaint_Rate", size="Revenue",
    color="Group", color_discrete_map=colors, category_orders=group_order,
    hover_name="Branch", hover_data=["Rating", "Repeat_Purchase_Rate"],
    title="สาขาใดมีเวลาบริการนานและอัตราร้องเรียนสูงร่วมกัน?",
)
fig.update_yaxes(tickformat=".1%")
st.plotly_chart(fig, width="stretch")

# Completed point 1: add three charts, each answering a different decision question.
complaint_chart = px.bar(
    summary.sort_values("Complaint_Rate", ascending=False),
    x="Branch", y="Complaint_Rate", color="Group",
    color_discrete_map=colors, category_orders=group_order,
    title="1. สาขาใดมีอัตราร้องเรียนเฉลี่ยสูงที่สุด?",
)
complaint_chart.update_xaxes(categoryorder="array", categoryarray=ranking["Branch"].tolist())
complaint_chart.update_yaxes(tickformat=".1%", rangemode="tozero")
st.plotly_chart(complaint_chart, width="stretch")

business_chart = px.bar(
    summary.melt(id_vars=["Branch", "Group"], value_vars=["Revenue", "Profit"],
                 var_name="Metric", value_name="Amount"),
    x="Branch", y="Amount", color="Group", facet_col="Metric",
    color_discrete_map=colors, category_orders=group_order,
    title="2. สาขาที่เสนอมีรายได้และกำไรขนาดเท่าใด?",
)
business_chart.update_xaxes(categoryorder="array", categoryarray=ranking["Branch"].tolist())
business_chart.update_yaxes(rangemode="tozero")
st.plotly_chart(business_chart, width="stretch")

customer_chart = px.scatter(
    summary, x="Repeat_Purchase_Rate", y="Rating", color="Group",
    color_discrete_map=colors, category_orders=group_order, hover_name="Branch",
    title="3. ผลลัพธ์ด้านซื้อซ้ำและคะแนนประเมินของสาขาที่เสนอเป็นอย่างไร?",
)
customer_chart.update_xaxes(tickformat=".0%")
customer_chart.update_yaxes(range=[0, 5])
st.plotly_chart(customer_chart, width="stretch")

# Completed point 2: all evidence values and comparative words come from the data.
def comparison(metric, percent=False):
    chosen, peer = selected[metric].mean(), others[metric].mean()
    direction = "สูงกว่า" if chosen > peer else "ต่ำกว่า" if chosen < peer else "เท่ากับ"
    value_format = ".1%" if percent else ".2f"
    return f"{chosen:{value_format}} {direction}สาขาอื่น ({peer:{value_format}})"


revenue_share = selected["Revenue"].sum() / summary["Revenue"].sum()
st.subheader("Evidence-based Insight Headlines")
st.markdown(f"**1. กลุ่มที่ควรตรวจปัญหาบริการก่อน: {branch_names}**")
st.write(
    f"Evidence: อัตราร้องเรียนเฉลี่ย {comparison('Complaint_Rate', True)}; "
    f"เวลาบริการเฉลี่ย {comparison('Service_Time_Min')} นาที"
)
st.write("Insight: ใช้ลำดับนี้เลือกพื้นที่ตรวจหน้างานก่อน ยังสรุปไม่ได้ว่าเวลาบริการเป็นสาเหตุของการร้องเรียน")
st.markdown(f"**2. กลุ่มที่เสนอมีรายได้คิดเป็น {revenue_share:.1%} ของรายได้รวม**")
st.write(
    f"Evidence: รายได้ {selected['Revenue'].sum():,.2f}; "
    f"กำไร {selected['Profit'].sum():,.2f} ในชุดข้อมูลนี้"
)
st.write("Insight: ตัวเลขนี้บอกขนาดธุรกิจที่เกี่ยวข้อง ไม่ใช่รายได้ที่จะเพิ่มขึ้นหรือกำไรที่จะได้จากการลงทุน")
st.markdown("**3. ตรวจผลลัพธ์ด้านลูกค้าควบคู่กับการแก้กระบวนการ**")
st.write(
    f"Evidence: อัตราซื้อซ้ำเฉลี่ย {comparison('Repeat_Purchase_Rate', True)}; "
    f"คะแนนประเมินเฉลี่ย {comparison('Rating')}"
)
st.write("Insight: ใช้ติดตามว่าการปรับบริการมาพร้อมผลลัพธ์ด้านลูกค้าที่ดีขึ้นหรือไม่ ต้องเก็บข้อมูลหลังทดลองเพิ่มเติม")

# Completed point 3: evidence -> provisional recommendation -> validation.
st.header("Recommendation")
st.info(
    f"เสนอ {branch_names} เป็น 3 สาขาสำหรับทดลองปรับปรุงบริการ 30 วัน "
    "ตามเกณฑ์อัตราร้องเรียน เริ่มตรวจสาเหตุจากบันทึกข้อร้องเรียนและเวลารอแต่ละขั้นตอน "
    "แล้วทดลองปรับคิว/ขั้นตอนบริการตามปัญหาที่พบ"
)
st.write(
    "ก่อนอนุมัติงบ ให้ตรวจนิยามข้อมูล ช่วงเวลาที่เก็บ ความต่างของ Customer Segment "
    "และต้นทุนปรับปรุงรายสาขา หลังทดลองให้ทบทวนผลวันที่ 30 ก่อนขยายผล "
    "ข้อมูลนี้ยังระบุสาเหตุหรือคำนวณ ROI ไม่ได้"
)

# Completed point 4: one measurable plan per selected branch, using its own baseline.
# Management assumptions for the exercise, NOT predictions from the historical CSV.
COMPLAINT_REDUCTION = 0.20
SERVICE_TIME_REDUCTION = 0.15
action_rows = []
for row in selected.itertuples(index=False):
    action_rows.append({
        "Branch": row.Branch,
        "Action": "ตรวจข้อร้องเรียน/เวลารอ แล้วทดลองปรับคิวและขั้นตอนตามสาเหตุที่พบ",
        "Owner": f"ผู้จัดการ {row.Branch} ร่วมกับ Operations Manager",
        "Timeline": "วัน 1–7 ตรวจสาเหตุ; วัน 8–30 ทดลอง; ทบทวนวันที่ 30",
        "KPI": "Complaint Rate; Service Time; ติดตาม Rating / Repeat Purchase ควบคู่",
        "Baseline": (
            f"Complaint {row.Complaint_Rate:.2%}; Service {row.Service_Time_Min:.2f} นาที; "
            f"Rating {row.Rating:.2f}; Repeat {row.Repeat_Purchase_Rate:.2%}"
        ),
        "Target": (
            f"Complaint ≤ {row.Complaint_Rate * (1 - COMPLAINT_REDUCTION):.2%}; "
            f"Service ≤ {row.Service_Time_Min * (1 - SERVICE_TIME_REDUCTION):.2f} นาที"
        ),
        "Expected Impact": "คาดหวังให้ร้องเรียนและเวลารอลดลง; ต้องวัดผลจริง ยังไม่ประมาณกำไรเพิ่ม",
    })
action_plan = pd.DataFrame(action_rows)
st.header("Action Plan")
st.caption(
    "Owner เป็นบทบาทที่เสนอ; Target เป็นสมมติฐานเพื่อฝึกวางแผน: "
    "ลดอัตราร้องเรียน 20% แบบสัมพัทธ์ และลดเวลาบริการ 15% จาก baseline รายสาขา "
    "ต้องตกลงความเป็นไปได้กับผู้รับผิดชอบก่อนใช้จริง"
)
st.dataframe(action_plan, width="stretch", hide_index=True)
st.write(
    "การวัดผล: เก็บจำนวนข้อร้องเรียนและตัวหารจริง พร้อมเวลาบริการและวันเวลา "
    "เปรียบเทียบก่อน/หลังด้วยนิยามเดียวกันและช่วงเวลาที่เทียบกันได้ "
    "ติดตามกลุ่มสาขาอื่นและสัดส่วนลูกค้าประกอบ; ผลก่อน/หลังเพียงอย่างเดียวยังไม่พิสูจน์เหตุและผล"
)

with st.expander("Prompt และแนวคิดสำหรับเติมแต่ละจุด"):
    st.markdown(Path(__file__).with_name("example_app_guide.md").read_text(encoding="utf-8"))

with st.expander("ตัวอย่างขั้นตอนวิเคราะห์ข้อมูลและกราฟ 8 แนวทาง"):
    st.markdown(Path(__file__).with_name("example_analysis_guide.md").read_text(encoding="utf-8"))

with st.expander("ดูโค้ดวิเคราะห์ฉบับเต็มที่นำไปรันได้"):
    st.code(Path(__file__).with_name("example_analysis.py").read_text(encoding="utf-8"), language="python")
