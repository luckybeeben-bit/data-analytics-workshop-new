# LAB 04 — Pandas Fundamentals: จาก Spreadsheet สู่ Reproducible Analysis
**Day 2 | ANALYZE & INTERPRET**  
**เวลา:** 55 นาที | **รูปแบบ:** Individual | **เครื่องมือ:** GitHub Codespaces, VS Code, Python/Pandas

## เป้าหมายของ Lab
ให้ผู้เรียนสามารถเปิด Dataset, ตรวจโครงสร้าง และสรุปข้อมูลด้วย Pandas โดยเข้าใจว่าแต่ละคำสั่งช่วยตอบ Business Question อย่างไร

> เป้าหมายไม่ใช่ “จำ Syntax” แต่คือสามารถอ่าน/ปรับ Code เพื่อวิเคราะห์ข้อมูลของตนเองได้

---

## ไฟล์ที่ใช้

```text
day02/case02_marketing/data/marketing_performance.csv
day02/starter/analysis_starter.py
```

---

# ก่อนเริ่ม — ตรวจ Workspace (5 นาที)
1. เปิด Repository ใน Codespaces
2. ดู Explorer ด้านซ้ายว่ามี `day02/`
3. เปิด Terminal
4. ตรวจ current folder:

```bash
pwd
```

5. ตรวจ Python/Pandas:

```bash
python --version
python -c "import pandas as pd; print(pd.__version__)"
```

ถ้าไม่ผ่าน ให้หยุดและแจ้งผู้สอน

---

# ขั้นตอนการทดลอง

## Step 1 — เปิด Starter Script และ Run ครั้งแรก (5 นาที)
เปิด:

```text
day02/starter/analysis_starter.py
```

Run:

```bash
python day02/starter/analysis_starter.py
```

### ควรเห็น
- 5 แถวแรก
- รายชื่อ columns
- data type
- จำนวน rows ที่ไม่เป็น null

### ถ้า FileNotFoundError
ตรวจว่า run จาก root ของ repository หรือไม่

---

## Step 2 — อ่านข้อมูลด้วย `read_csv()` และดูตัวอย่าง (5 นาที)
Code:

```python
import pandas as pd

df = pd.read_csv("day02/case02_marketing/data/marketing_performance.csv")
print(df.head())
```

เขียนคำตอบ:

```text
หนึ่งแถวของ Dataset นี้แทนอะไร?
____________________________________
```

> การรู้ “grain” หรือความหมายของ 1 row สำคัญมากก่อน groupby

---

## Step 3 — ตรวจโครงสร้างด้วย `info()` (5 นาที)

```python
df.info()
```

สังเกต:
- จำนวน rows/columns
- data type
- null count โดยคร่าว

ตอบ:

```text
Column ใดเป็น Dimension?
Column ใดเป็น Metric?
Column ใดควรเป็น Date?
```

---

## Step 4 — สรุป Numeric ด้วย `describe()` (5 นาที)

```python
print(df.describe())
```

อย่าอ่านทุกตัวเลข ให้หาเพียง:
- ค่าที่ดูสูง/ต่ำผิดปกติ
- ช่วงของ Spend/Revenue/ROAS
- สิ่งที่ควรตรวจเพิ่ม

### Checkpoint
`describe()` ไม่ตอบ Business Question โดยตรง แต่ช่วย “รู้จักข้อมูล” ก่อนวิเคราะห์

---

## Step 5 — Data Quality Check แบบสั้น (5 นาที)

```python
print(df.isnull().sum())
print("duplicates:", df.duplicated().sum())
```

ตรวจ category:

```python
print(df["Channel"].value_counts())
print(df["Customer_Segment"].value_counts())
```

### Reflection
สิ่งที่ Google Sheets ทำด้วย Filter/Pivot เมื่อวาน วันนี้ Python ทำซ้ำได้ด้วย Code

---

## Step 6 — Filter ด้วย `query()` (5 นาที)
ตัวอย่าง:

```python
email = df.query("Channel == 'Email'")
print(email.head())
```

ลอง Filter:

```python
high_roas = df.query("ROAS > 3")
```

ตอบ:

> Filter นี้ช่วยตอบคำถามอะไร?

---

## Step 7 — Groupby ครั้งแรก (8 นาที)

```python
channel_summary = (
    df.groupby("Channel", as_index=False)
      .agg(
          Spend=("Spend", "sum"),
          Revenue=("Revenue", "sum"),
          Conversions=("Conversions", "sum")
      )
)

print(channel_summary)
```

### อ่าน Code ทีละส่วน
- `groupby("Channel")` → แบ่งข้อมูลตาม Channel
- `.agg(...)` → สรุป Metric ของแต่ละกลุ่ม
- `as_index=False` → ให้ Channel ยังเป็น column ปกติ

### Business Purpose
> เปรียบเทียบ scale ของ Spend/Revenue/Conversions ระหว่าง Channel

---

## Step 8 — Sort เพื่อ Rank (5 นาที)

```python
print(channel_summary.sort_values("Revenue", ascending=False))
```

ลองเปลี่ยนเป็น Sort ด้วย Spend หรือ metric อื่น

### คำถาม
Ranking เปลี่ยนไหมเมื่อเปลี่ยน Metric?

นี่คือสัญญาณว่าไม่ควรตัดสินใจจาก metric เดียว

---

## Step 9 — Save Output (4 นาที)
สร้าง folder ถ้ายังไม่มี:

```bash
mkdir -p day02/output
```

ใน Python:

```python
channel_summary.to_csv("day02/output/channel_summary.csv", index=False)
```

ตรวจใน Explorer ว่าไฟล์ถูกสร้าง

---

# Stop & Explain
ผู้สอนอาจสุ่มถาม:

> `groupby()` block นี้ Input คืออะไร → ทำอะไร → Output คืออะไร → ช่วย Decision อย่างไร?

ห้ามตอบเพียง “Copilot เขียนให้”

---

# สิ่งที่ต้องส่ง
- Script ที่ run ได้
- `channel_summary.csv`
- คำอธิบาย Code 1 block ด้วยภาษาของตนเอง
- Business Purpose ของคำสั่งสำคัญ ≥3 จุด

---

# Core / Challenge

## Core
ทำ Step 1–9 ให้ครบ

## Challenge
สร้าง function:

```python
def summarize_by(df, dimension):
    # return Spend / Revenue / Conversions summary
    ...
```

แล้วทดลองกับ `Channel` และ `Customer_Segment`

---

# Common Mistakes
- Run script จาก folder ผิดจนหา CSV ไม่เจอ
- ใช้ `mean()` กับ Metric ที่ควร sum โดยไม่คิด Business Meaning
- Groupby ก่อนรู้ว่า 1 row หมายถึงอะไร
- Copy code จาก AI แล้วอธิบายไม่ได้

**จำไว้:** Reproducible Analytics = คนอื่น Run code เดิมแล้วได้วิธีวิเคราะห์เดียวกัน
