# LAB 05 — Segment / Compare / Rank: อย่าตัดสินใจจาก Metric เดียว
**Day 2 | ANALYZE & INTERPRET**  
**เวลา:** 75 นาที | **รูปแบบ:** Individual | **เครื่องมือ:** Python/Pandas + Codespaces

## เป้าหมายของ Lab
วิเคราะห์ Marketing Performance โดยเปรียบเทียบ **Scale + Efficiency + Segment** เพื่อค้นหา Trade-off ก่อนเสนอ Budget Allocation

Business Decision:

> Channel และ Customer Segment ใดควรได้รับงบเพิ่ม/ลด?

---

## Dataset

```text
day02/case02_marketing/data/marketing_performance.csv
```

ใช้ script ต่อจาก LAB 04 หรือสร้างไฟล์ใหม่ใน `day02/output/`

---

# ขั้นตอนการทดลอง

## Step 1 — เขียน Decision Criteria ก่อน Code (5 นาที)
ก่อน Run อะไร ให้เขียนว่า Budget Decision ควรดูอย่างน้อยอะไรบ้าง

ตัวอย่าง:

```text
Scale: Spend, Revenue, Conversions
Efficiency: ROAS, Conversion Rate
Segment: Customer_Segment
Stability: จำนวน records / scale เพียงพอหรือไม่
```

### Checkpoint
ถ้าเขียนเพียง “ROAS” ให้เพิ่มอย่างน้อยอีก 2 มิติ

---

## Step 2 — Channel Summary: Scale (10 นาที)

```python
channel_scale = (
    df.groupby("Channel", as_index=False)
      .agg(
          Spend=("Spend", "sum"),
          Revenue=("Revenue", "sum"),
          Conversions=("Conversions", "sum"),
          Campaign_Rows=("Campaign", "count")
      )
)
```

เพิ่ม ROAS จากยอดรวม:

```python
channel_scale["ROAS_calc"] = channel_scale["Revenue"] / channel_scale["Spend"]
```

> ระวัง: การเฉลี่ย ROAS รายแถวอาจไม่เท่ากับ Total Revenue / Total Spend

เรียงลำดับ:

```python
print(channel_scale.sort_values("Revenue", ascending=False))
print(channel_scale.sort_values("ROAS_calc", ascending=False))
```

### คำถาม
Channel อันดับ 1 เปลี่ยนหรือไม่เมื่อ Rank ด้วย Revenue เทียบกับ ROAS?

---

## Step 3 — Segment Summary (10 นาที)

```python
segment_summary = (
    df.groupby("Customer_Segment", as_index=False)
      .agg(
          Spend=("Spend", "sum"),
          Revenue=("Revenue", "sum"),
          Conversions=("Conversions", "sum"),
          Avg_Conversion_Rate=("Conversion_Rate", "mean")
      )
)
```

คำนวณ:

```python
segment_summary["ROAS_calc"] = segment_summary["Revenue"] / segment_summary["Spend"]
```

ตอบ:
- Segment ใดมี Revenue สูง?
- Segment ใด efficiency สูง?
- Segment ใดมี scale เล็กแต่ performance น่าสนใจ?

---

## Step 4 — Channel × Segment (15 นาที)
วิเคราะห์ 2 dimensions:

```python
channel_segment = (
    df.groupby(["Channel", "Customer_Segment"], as_index=False)
      .agg(
          Spend=("Spend", "sum"),
          Revenue=("Revenue", "sum"),
          Conversions=("Conversions", "sum")
      )
)
channel_segment["ROAS_calc"] = channel_segment["Revenue"] / channel_segment["Spend"]
```

เรียง:

```python
print(channel_segment.sort_values("ROAS_calc", ascending=False).head(10))
```

### Checkpoint
หา 1 combination ที่:
- ROAS สูง แต่ Spend/Revenue scale เล็ก
- หรือ Revenue สูง แต่ ROAS ไม่สูงสุด

นี่คือ **Trade-off Evidence**

---

## Step 5 — ตรวจ Trend ตามเวลา (10 นาที)
ก่อน groupby ให้แปลง Month:

```python
df["Month"] = pd.to_datetime(df["Month"])
```

สรุป:

```python
monthly_channel = (
    df.groupby(["Month", "Channel"], as_index=False)
      .agg(Spend=("Spend", "sum"), Revenue=("Revenue", "sum"))
)
monthly_channel["ROAS_calc"] = monthly_channel["Revenue"] / monthly_channel["Spend"]
```

ถาม:
> Channel ที่ดูดีในภาพรวม ดีสม่ำเสมอทุกเดือนหรือไม่?

อย่าดูเพียงค่าเฉลี่ยรวม

---

## Step 6 — สร้าง Evidence Table (10 นาที)
สร้างตารางอย่างน้อย 3 Evidence:

| Question | Metric/Comparison | Evidence | Interpretation |
|---|---|---|---|
| Channel ไหน scale สูง? | Revenue/Conversions | | |
| Channel ไหน efficient? | ROAS | | |
| Segment ไหนน่าสนใจ? | Channel×Segment | | |

### กติกา
Evidence = สิ่งที่เห็นจาก output  
Interpretation = ความหมายที่คุณตีความ

อย่าผสมสองอย่างเป็นประโยคเดียวโดยไม่รู้ตัว

---

## Step 7 — Recommendation Draft แบบ “ยังไม่ Final” (10 นาที)
เขียนเพียง Draft:

```text
Based on current evidence, I would TEST increasing ______,
because ______.
However, I would verify ______ before scaling the budget.
```

คำว่า **TEST** สำคัญ เพราะ observational data ยังไม่ได้พิสูจน์ diminishing return

---

## Step 8 — Save Analysis Outputs (5 นาที)

```python
channel_scale.to_csv("day02/output/channel_scale.csv", index=False)
segment_summary.to_csv("day02/output/segment_summary.csv", index=False)
channel_segment.to_csv("day02/output/channel_segment.csv", index=False)
```

---

# Stop & Share
เตรียมตอบ:

> “ถ้าดู Revenue อย่างเดียว ฉันจะเลือก ______ แต่เมื่อดู ROAS/Segment เพิ่ม ฉันพบว่า ______”

---

# สิ่งที่ต้องส่ง
- Channel summary
- Segment summary
- Channel × Segment summary
- Evidence ≥3
- Trade-off ≥1
- Draft recommendation + สิ่งที่ต้อง Verify เพิ่ม

---

# Core / Challenge

## Core
ทำ Scale + Efficiency + Segment

## Challenge
สร้าง Plotly chart หรือ small multiple เพื่อเปรียบเทียบ Revenue vs ROAS และใช้ bubble size เป็น Spend

---

# Common Mistakes
- ใช้ Revenue อย่างเดียว
- ใช้ ROAS อย่างเดียว
- เฉลี่ย ratio โดยไม่คิด weighting
- เห็น performance สูงแล้วสรุปว่าเพิ่ม Budget จะได้ผลเท่าเดิม

**จำไว้:** Rank เปลี่ยนเมื่อ Metric เปลี่ยน = Decision ต้องเห็น Trade-off
