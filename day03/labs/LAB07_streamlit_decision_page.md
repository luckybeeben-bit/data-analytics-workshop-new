# LAB 07 — Executive Decision Web App: จาก Analysis สู่สิ่งที่ผู้บริหารใช้ตัดสินใจได้
**Day 3 | COMMUNICATE & DECIDE**  
**เวลารวม:** ประมาณ 150 นาที | **รูปแบบ:** Individual + Peer Review  
**เครื่องมือ:** Python/Pandas, Plotly, Streamlit, GitHub Copilot

## เป้าหมายของ Lab
สร้าง **Executive Decision Page** ที่ตอบคำถามบริหารได้ในเวลาสั้น ๆ โดยใช้ผลวิเคราะห์จริง ไม่ใช่สร้าง Dashboard ที่มีกราฟจำนวนมาก

ผู้บริหารควรเปิดหน้าเว็บแล้วเข้าใจภายใน ~60 วินาทีว่า:
1. ต้องตัดสินใจอะไร
2. ปัญหาอยู่ตรงไหน
3. Evidence สำคัญคืออะไร
4. คุณเสนอให้ทำอะไร
5. จะวัดผล Action อย่างไร

---

## ไฟล์ที่ใช้

```text
day03/case03_branch/CASE_BRIEF.md
day03/case03_branch/data/branch_customer_performance.csv
day03/app_starter/app.py
```

---

# ขั้นตอนการทดลอง

## Step 1 — อ่าน Decision ก่อนเปิด App (10 นาที)
Decision:

> บริษัทมีงบปรับปรุงเพียง 3 สาขา ควรเลือกสาขาใด และควรแก้ปัญหาอะไร?

เขียนก่อน:

```text
Decision Question:
____________________________________________

Top 3 metrics I expect to matter:
1. __________
2. __________
3. __________
```

ห้ามเริ่มจาก “อยากทำกราฟอะไร”

---

## Step 2 — Run Starter App (10 นาที)
จาก repository root:

```bash
streamlit run day03/app_starter/app.py
```

Codespaces ควรเปิด forwarded port 8501

ถ้าไม่เปิดอัตโนมัติ:
- ดู tab `PORTS`
- หา port `8501`
- กด Open in Browser

### Checkpoint 1
ควรเห็น:
- Page title
- Decision Question
- KPI cards
- Scatter plot
- Placeholder Recommendation/Action Plan

---

## Step 3 — อ่าน Starter Code ก่อนแก้ (10 นาที)
เปิด `app.py` แล้วหา 5 ส่วน:

1. `read_csv`
2. `groupby("Branch")`
3. KPI metrics
4. Plotly chart
5. Recommendation/Action placeholders

ตอบ:

> KPI ตอนนี้ช่วย Decision เพียงพอหรือยัง?

ตัวอย่าง: `Total Revenue` อาจเป็น context แต่ยังไม่ได้บอกว่าสาขาใดควรปรับปรุง

---

## Step 4 — สร้าง Branch Summary ที่เชื่อถือได้ (15 นาที)
ตรวจ aggregation เช่น:

```python
summary = (
    df.groupby("Branch", as_index=False)
      .agg(
          Revenue=("Revenue", "sum"),
          Profit=("Profit", "sum"),
          Orders=("Orders", "sum"),
          Rating=("Rating", "mean"),
          Repeat_Purchase_Rate=("Repeat_Purchase_Rate", "mean"),
          Complaint_Rate=("Complaint_Rate", "mean"),
          Service_Time_Min=("Service_Time_Min", "mean")
      )
)
```

### ถามก่อนใช้ค่าเฉลี่ย
แต่ละ row มีน้ำหนักเท่ากันจริงหรือไม่? หากมี volume ต่างกันมาก อาจต้องพิจารณา weighted metric ในงานจริง

สำหรับ Workshop ให้ใช้ aggregation นี้เป็น starting point และระบุ limitation หากจำเป็น

---

## Step 5 — เลือก KPI 3–5 ตัวที่ช่วย Decision (15 นาที)
แยกเป็น:

### Context KPI
- Total Revenue
- Total Profit

### Decision KPI
- Complaint Rate
- Service Time
- Repeat Purchase
- Rating

อย่าใส่ KPI เพียงเพราะคำนวณได้

เขียนเหตุผล:

| KPI | ช่วย Decision อย่างไร? |
|---|---|
| Complaint Rate | บอก severity ของ service issue |
| Service Time | สะท้อน operational friction |
| ... | ... |

---

## Step 6 — สร้าง Evidence Ranking Table (15 นาที)
ก่อนสร้างกราฟหลายชิ้น ให้ทำ table ที่ใช้ rank

ตัวอย่าง:

```python
risk_table = summary.sort_values(
    ["Complaint_Rate", "Service_Time_Min"],
    ascending=[False, False]
)
```

หรือสร้าง simple score เพื่อช่วยสำรวจ แต่ต้องระวังว่า weight เป็น assumption

```python
# ตัวอย่างเพื่อการเรียนรู้ ไม่ใช่สูตรสากล
summary["Risk_Score"] = (
    summary["Complaint_Rate"].rank(pct=True) +
    summary["Service_Time_Min"].rank(pct=True) -
    summary["Repeat_Purchase_Rate"].rank(pct=True)
)
```

### สำคัญ
ถ้าใช้ Risk Score ต้องบอกว่าเป็น **Analyst-defined heuristic** ไม่ใช่ “ความจริงจากข้อมูล”

---

## Step 7 — สร้าง Evidence Visualization 2–4 ชิ้น (20 นาที)
เลือกเฉพาะกราฟที่ตอบคำถามต่างกัน

### Chart A — Service Time vs Complaint
ใช้เพื่อดูว่าปัญหา 2 ด้านเกิดร่วมกันที่สาขาใด

### Chart B — Branch Profit/Revenue Context
ใช้ดู Business Impact ของสาขาที่มี service issue

### Chart C — Repeat Purchase / Rating
ใช้ดู Customer outcome

ใช้ Copilot ช่วย implementation ได้ เช่น:

```text
Add a Plotly bar chart to app.py showing Complaint_Rate by Branch,
sorted from highest to lowest.
Use the existing `summary` dataframe.
Do not hard-code branch names or conclusions.
Explain the code before editing.
```

### Chart Rule
ก่อนเพิ่มแต่ละกราฟ เขียน:

```text
This chart helps answer:
________________________________________
```

---

## Step 8 — เปลี่ยน Chart Title ให้เป็น Insight Headline (10 นาที)
ไม่ใช้:

> Complaint Rate by Branch

ถ้า Evidence รองรับ อาจใช้:

> A small group of branches shows both elevated complaints and longer service time

หรือข้อความไทยที่ไม่สรุปเกินข้อมูล

### ห้าม
อย่าเขียนว่า “พนักงานไม่พอจึงเกิด Complaint” หากยังไม่มี staffing evidence

---

## Step 9 — เขียน Evidence → Insight → Recommendation (15 นาที)
ใช้ E-I-R-A:

### Evidence
ตัวเลข/Comparison ที่ตรวจได้

### Insight
สิ่งนี้มีความหมายต่อ Decision อย่างไร

### Recommendation
ควร “ทดลอง/ตรวจ/ดำเนินการ” อะไร

### Action
ใครทำ เมื่อไร KPI/Target อะไร

ตัวอย่างโครง:

```text
Evidence:
Branches ___ show higher complaint rate and service time than peers.

Insight:
The service problem appears concentrated rather than company-wide.

Recommendation:
Prioritize a service-process pilot in the highest-risk branches before company-wide rollout.
```

---

## Step 10 — สร้าง Action Plan ที่วัดผลได้ (15 นาที)
หน้าเว็บต้องมี:

| Action | Owner | Timeline | KPI | Baseline | Target | Expected Impact |
|---|---|---|---|---|---|---|

ตัวอย่าง:

```text
Action: ทดลองปรับ Queue/Staff Allocation
Owner: Operations Manager
Timeline: 30 วัน
KPI: Service Time, Complaint Rate
Baseline: จากข้อมูลปัจจุบัน
Target: กำหนดให้สมเหตุสมผลและระบุว่าเป็น management target
```

### ระวัง Target
ข้อมูลย้อนหลังไม่ได้ “บอก” Target โดยอัตโนมัติ  
Target มักเป็น Decision/Management assumption ต้องระบุที่มา

---

## Step 11 — 60-second Executive Test (15 นาที)
จับคู่กับเพื่อน

ผู้ทดลอง A เปิด App ของ B **60 วินาทีโดยไม่ให้ B อธิบาย**

แล้วตอบ 3 ข้อ:
1. ผู้บริหารต้องตัดสินใจอะไร?
2. Evidence สำคัญที่สุดคืออะไร?
3. เจ้าของ App เสนอให้ทำอะไร?

ให้คะแนน:

```text
3/3 = ชัด
2/3 = ต้องปรับ hierarchy
0–1/3 = ยังเป็น dashboard มากกว่า decision page
```

สลับกัน

---

## Step 12 — Revise: ตัดสิ่งที่ไม่ช่วย Decision (10 นาที)
ก่อนจบ ให้ลบอย่างน้อย 1 อย่างที่ไม่จำเป็น เช่น:
- chart ซ้ำ
- KPI ไม่เกี่ยว
- paragraph ยาว
- decorative element

> การตัดคือส่วนหนึ่งของ Data Storytelling

---

## Step 13 — Final Run & Commit (5 นาที)
ตรวจว่า App run โดยไม่มี error

```bash
git status
git add .
git commit -m "Complete Lab07 executive decision app"
```

---

# สิ่งที่ต้องส่ง
Executive Decision Web App ที่มี:

- [ ] Decision Question 1 ข้อ
- [ ] Executive KPIs 3–5
- [ ] Evidence Visualizations ไม่เกิน 4
- [ ] Evidence 3–5 ข้อ
- [ ] Insight 2–3 ข้อ
- [ ] Recommendation 1–2 ข้อ
- [ ] Action Plan ที่มี Owner / Timeline / KPI / Target
- [ ] ผล 60-second Peer Test

---

# Core / Challenge

## Core
สร้าง App จาก Starter ให้ตอบ Decision ได้ครบ

## Challenge
เพิ่ม:
- filter ที่ช่วย Decision จริง
- scenario comparison
- downloadable evidence table

แต่ต้องไม่เพิ่ม feature จนทำให้ Executive Page ซับซ้อนขึ้นโดยไม่จำเป็น

---

# Common Mistakes
- ทำเว็บสวย แต่ไม่รู้ Decision Question
- สร้างกราฟ 8–10 ชิ้นเพราะ AI ทำให้ได้
- hard-code ชื่อ “สาขาที่แย่” แทนคำนวณจาก data
- Recommendation ไม่มี Evidence
- Target ถูกแต่งขึ้นแต่เขียนเหมือนเป็นสิ่งที่ data พิสูจน์

**จำไว้:** Web App คือ Decision Interface ไม่ใช่ผลงานโชว์ความสามารถด้าน Frontend
