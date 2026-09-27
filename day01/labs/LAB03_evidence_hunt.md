# LAB 03 — Evidence Hunt: จากข้อมูลสู่ข้อความที่ตรวจสอบย้อนกลับได้
**Day 1 | QUESTION & EVIDENCE**  
**เวลา:** 90 นาที | **รูปแบบ:** Individual | **เครื่องมือ:** Google Sheets

## เป้าหมายของ Lab
ใช้ข้อมูลที่ผ่านการตรวจคุณภาพแล้วเพื่อค้นหา Pattern และเขียน **Evidence Statement** ที่คนอื่นสามารถย้อนกลับไปตรวจในข้อมูลได้

เมื่อจบ Lab นี้ คุณควรมี:
- Pivot/summary อย่างน้อย 2 ชุด
- Visualization อย่างน้อย 2 แบบ
- Evidence Statements อย่างน้อย 3 ข้อ
- Insight 2 ข้อ
- Hypothesis 1 ข้อ
- รายการสิ่งที่จะวิเคราะห์ต่อ

---

## Dataset
ใช้ `Working_Data` จาก LAB 02

> ถ้ายัง Cleaning ไม่เสร็จ ให้ใช้เฉพาะส่วนที่ตรวจแล้ว และเขียน Limitation ไว้

---

# ขั้นตอนการทดลอง

## Step 1 — กลับไปอ่าน Analytical Question ของ LAB 01 (5 นาที)
เลือกคำถามหลัก 2–3 ข้อที่ต้องการตอบ

เขียนไว้ด้านบนของ worksheet เช่น:

```text
Q1: Region ใดมี Profit ต่ำที่สุด?
Q2: Product ใด Sales สูงแต่ Profit ต่ำ?
Q3: Discount ระดับสูงสัมพันธ์กับ Profit/Margin อย่างไร?
```

> ถ้า Analysis ไม่ตอบคำถามใดเลย แสดงว่ากำลัง “สำรวจไปเรื่อย” มากเกินไป

---

## Step 2 — สร้าง Pivot 1: Region × Performance (15 นาที)
ใน Google Sheets:
1. เลือกข้อมูลทั้งหมด
2. `Insert → Pivot table`
3. สร้างใน New Sheet ชื่อ `PVT_Region`
4. Rows → `Region`
5. Values → `Sales` → SUM
6. Values → `Profit` → SUM
7. เพิ่ม `Quantity` หรือ Metric อื่นตามคำถาม

### เพิ่ม Profit Margin แบบง่าย
ถ้าจะใช้ Margin ต้องระวังว่า:

```text
Total Margin = SUM(Profit) / SUM(Sales)
```

ไม่ควรเฉลี่ย Margin รายแถวแบบไม่คิดน้ำหนัก

### Checkpoint 1
ตอบได้หรือยังว่า:
- Region ใด Sales สูงสุด?
- Region ใด Profit ต่ำ?
- Sales สูง = Profit สูงเสมอหรือไม่?

---

## Step 3 — Drill down Region → Product (15 นาที)
สร้าง Pivot ใหม่ `PVT_Region_Product`

ตัวอย่าง setup:
- Rows → Region
- Rows เพิ่ม → Product หรือ Category
- Values → Sales
- Values → Profit

ใช้ Filter เพื่อดู Region ที่สงสัย

### คำถาม
> ปัญหาเกิดทั้ง Region หรือกระจุกที่ Product/Category บางกลุ่ม?

นี่คือจุดเปลี่ยนจาก “Region แย่” ไปสู่ Insight ที่ละเอียดขึ้น

---

## Step 4 — ตรวจ Discount กับ Profit (15 นาที)
เลือกวิธีใดวิธีหนึ่ง

### วิธี A — สร้าง Discount Band
เพิ่ม column ใหม่ เช่น `Discount_Band`

แนวคิด:

```text
0–5%
>5–10%
>10–15%
>15%
```

จากนั้น Pivot:
- Rows → Discount_Band
- Values → Average/SUM Profit หรือ Margin ที่คำนวณเหมาะสม

### วิธี B — Scatter Plot
1. เลือก Discount และ Profit
2. `Insert → Chart`
3. Chart type → Scatter chart
4. ตรวจว่ามี outlier หรือ cluster หรือไม่

### ห้ามสรุป
ถ้า Discount สูงและ Profit ต่ำ อย่าเพิ่งเขียนว่า:

> Discount **ทำให้** Profit ต่ำ

ควรเขียนว่า:

> กลุ่ม Discount สูง **มีแนวโน้ม** Profit/Margin ต่ำกว่า และควรตรวจ Product Mix/Cost เพิ่ม

---

## Step 5 — สร้าง Visualization ที่ตอบ Decision (10 นาที)
เลือก Chart เพียง 2 แบบที่ช่วย Decision จริง

ตัวอย่าง:
- Bar chart → Profit by Region/Product
- Scatter → Discount vs Profit
- Line → Trend ตาม Date ถ้าคำถามเกี่ยวกับเวลา

ก่อนสร้างทุกกราฟ ให้เขียน:

```text
Decision purpose of this chart:
________________________________________
```

ถ้าตอบไม่ได้ ไม่ต้องสร้างกราฟนั้น

---

## Step 6 — เขียน Evidence Statement ด้วยสูตร 5 ส่วน (15 นาที)
ใช้โครง:

> **Claim → Metric → Filter → Comparison → Evidence**

### ไม่ดี
> ภาคใต้แย่

### ดีขึ้น
> South มี Total Profit ต่ำกว่า Region อื่น และเมื่อ Drill down พบว่า Product P-B มีส่วนสำคัญต่อ Profit ที่ต่ำ

### ดีขึ้นอีก
> ใน Working Data ชุดนี้ South มี Total Profit ต่ำกว่าหลาย Region และ P-B เป็นกลุ่มที่มี Profit/Margin อ่อนกว่ากลุ่มอื่นใน South จึงควรตรวจ Discount และ Cost ของ P-B เพิ่ม

เขียนอย่างน้อย 3 Evidence Statements

```text
Evidence 1:

Evidence 2:

Evidence 3:
```

---

## Step 7 — แยก Evidence / Insight / Hypothesis / Recommendation (10 นาที)
ใช้ตารางนี้:

| ระดับ | คำตอบของคุณ |
|---|---|
| Evidence | ข้อมูลที่ตรวจย้อนกลับได้ |
| Insight | ความหมายเชิงธุรกิจจากหลาย Evidence |
| Hypothesis | คำอธิบายที่ยังต้องพิสูจน์ |
| Recommendation | สิ่งที่ควรทำ/วิเคราะห์ต่อ |

### ตัวอย่าง
- **Evidence:** South + Electronics มี Profit/Margin ต่ำกว่าหลายกลุ่ม
- **Insight:** ปัญหาดู concentrated ไม่ใช่ company-wide
- **Hypothesis:** Discount หรือ Cost/Product Mix อาจกด Margin
- **Recommendation:** ยังไม่ควรเพิ่ม Promotion ทั่วบริษัท ควรวิเคราะห์ Discount/Cost ก่อน

---

## Step 8 — เขียน “สิ่งที่ยังไม่รู้” (5 นาที)
เขียนอย่างน้อย 2 ข้อ เช่น:

- ไม่มี Campaign/Traffic/Conversion จึงยังบอกไม่ได้ว่า Marketing เป็นสาเหตุ
- ไม่มีข้อมูลคู่แข่ง/Seasonality เพียงพอ

นี่เป็นส่วนหนึ่งของ Analysis ที่ดี ไม่ใช่จุดอ่อน

---

# Stop & Share
เตรียมพูด 30 วินาที:

> “ข้อมูลชี้ว่า ______ แต่ยังสรุปไม่ได้ว่า ______ ดังนั้นควรตรวจ ______ เพิ่ม”

---

# สิ่งที่ต้องส่ง
- Pivot ≥2
- Charts 2 ชิ้น
- Evidence ≥3
- Insight 2
- Hypothesis 1
- Next Analysis ≥1

---

# Core / Challenge

## Core
Region/Product/Discount analysis ตามขั้นตอน

## Challenge
คำนวณ **Contribution to Profit Difference** หรือเปรียบเทียบ Period เพื่อดูว่า Product/Region ใด contribute ต่อการเปลี่ยนแปลงมากที่สุด

---

# Common Mistakes
- Chart title เป็นเพียง “Profit by Region” แทนการบอก Finding
- ใช้คำว่า “เพราะ” จาก Correlation
- Insight เป็นเพียงการอ่านตัวเลขซ้ำ
- Recommendation ไม่ย้อนกลับหา Evidence

**จำไว้:** Evidence ต้องตรวจย้อนกลับได้ และ Insight ต้องอธิบายว่า Evidence นั้น “มีความหมายอย่างไรต่อ Decision”
