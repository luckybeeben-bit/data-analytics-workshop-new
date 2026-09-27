# LAB 02 — Data Detective: ตรวจ Data Quality ก่อน Analysis
**Day 1 | QUESTION & EVIDENCE**  
**เวลา:** 75 นาที | **รูปแบบ:** Individual | **เครื่องมือ:** Google Sheets

## เป้าหมายของ Lab
ตรวจสอบว่าข้อมูลพร้อมสำหรับการวิเคราะห์หรือไม่ และฝึกตัดสินใจว่า Data Quality Issue แต่ละแบบควร **แก้ / Flag / ตรวจเพิ่ม / ไม่แตะต้อง** อย่างมีเหตุผล

เมื่อจบ Lab นี้ คุณควรมี:
- Working copy ของ Dataset
- Data Quality Log อย่างน้อย 5 รายการ
- ข้อมูลที่ปรับเฉพาะ Issue ที่มีเหตุผลรองรับ
- รายการ Issue ที่ยังต้อง Flag ไว้ ไม่เดาแก้เอง

---

## ไฟล์ที่ใช้

```text
day01/case01_retail/data/retail_sales_dirty.csv
```

> **หลักสำคัญ:** อย่าแก้ไฟล์ต้นฉบับโดยตรง ให้ทำสำเนาเสมอ

---

# ขั้นตอนการทดลอง

## Step 1 — นำ CSV เข้า Google Sheets (5 นาที)
1. เปิด Google Drive
2. `New → Google Sheets → Blank spreadsheet`
3. ตั้งชื่อ เช่น `Day1_DataDetective_<ชื่อ>`
4. เลือก `File → Import → Upload`
5. Upload `retail_sales_dirty.csv`
6. Import location เลือก **Replace spreadsheet** หรือ **Insert new sheet** ตามที่ผู้สอนกำหนด
7. เปลี่ยนชื่อ Tab เป็น `Raw_Data`
8. Duplicate Tab แล้วเปลี่ยนชื่อเป็น `Working_Data`

### Checkpoint 1
คุณควรมีอย่างน้อย 2 tabs:

```text
Raw_Data       ← ห้ามแก้
Working_Data   ← ใช้ทำความสะอาด
```

---

## Step 2 — ทำความเข้าใจคอลัมน์ก่อนแก้ข้อมูล (5 นาที)
อ่าน Header แล้วตอบสั้น ๆ ว่าแต่ละกลุ่มข้อมูลหมายถึงอะไร:

- `Date` → เวลา
- `Region`, `Branch` → Geography
- `Product`, `Category` → Product dimension
- `Customer_Segment` → Customer dimension
- `Quantity` → Volume
- `Discount` → ส่วนลด (ตรวจหน่วยให้ดี)
- `Sales`, `Cost`, `Profit` → Financial metrics

### คำถามก่อน Cleaning
> Discount = 0.10 หมายถึง 10% หรือ 0.10%?

ตรวจรูปแบบจากข้อมูลส่วนใหญ่ก่อนสรุป

---

## Step 3 — ตรวจ Missing Values (10 นาที)
วิธีที่ 1: เปิด Filter
1. เลือก Header row
2. `Data → Create a filter`
3. ที่แต่ละคอลัมน์ เลือก Filter → `Blanks`

วิธีที่ 2: ใช้สูตรช่วยนับ เช่น

```text
=COUNTBLANK(I2:I)
```

สำหรับคอลัมน์ `Sales`

บันทึก Issue ลง Data Quality Log:

| Issue | Field/Row | Evidence | Decision | Reason |
|---|---|---|---|---|
| Missing | Sales | พบ blank 1 row | Flag | ยังไม่มีข้อมูลพอให้เดา Sales |

### ห้ามทำ
อย่าใส่ค่าเฉลี่ยแทน Missing ทันทีเพียงเพราะ “ทำให้ตารางเต็ม”

---

## Step 4 — ตรวจ Duplicate (8 นาที)
1. เลือกข้อมูลทั้งหมด
2. ใช้ `Data → Data cleanup → Remove duplicates`
3. **ก่อนกดลบ** ให้ดูจำนวน duplicate ที่ระบบพบ
4. หากต้องการตรวจด้วยตา ให้ Sort ตามหลายคอลัมน์ เช่น Date + Branch + Product + Sales

### Decision
ถ้า record เหมือนกันทุก field อาจเป็น duplicate แต่ยังควรถาม:
- เป็น transaction ซ้ำจริงหรือไม่?
- มี Transaction ID หรือไม่?

ถ้าไม่มี ID ให้บันทึก Assumption ไว้

---

## Step 5 — ตรวจ Category Consistency (10 นาที)
ใช้ Filter หรือ Pivot เพื่อดู unique values ของ:

- Region
- Category
- Customer_Segment

ตัวอย่าง Issue:

```text
South
south
 SOUTH 
```

หรือ

```text
Electronics
Electronic
```

### วิธีแก้
- Trim ช่องว่าง
- Standardize ตัวพิมพ์เล็ก/ใหญ่
- ตรวจว่าคำต่างกันเป็น category เดียวกันจริงก่อนรวม

ตัวอย่างสูตรช่วยตรวจ:

```text
=TRIM(B2)
```

หรือ

```text
=UPPER(TRIM(B2))
```

> ไม่จำเป็นต้องใช้สูตรนี้เป็น final field เสมอ จุดสำคัญคือรู้ว่าเกิดความไม่สอดคล้อง

---

## Step 6 — ตรวจ Impossible / Suspicious Values (10 นาที)
ตรวจอย่างน้อย:

### Quantity
- มีค่าติดลบหรือไม่?
- ถ้ามี อาจเป็น Return หรือ Error?

### Discount
- ถ้าข้อมูลส่วนใหญ่เป็น 0–0.30 แล้วพบ 2.50 ควรตีความอย่างไร?

### Profit
ตรวจ logic ง่าย ๆ:

```text
Profit ≈ Sales - Cost
```

สร้าง helper column ชั่วคราวได้ เช่น:

```text
=I2-J2
```

แล้วเปรียบเทียบกับ Profit

### หลักการ
ค่าผิดปกติไม่เท่ากับค่าผิดเสมอ

`Outlier → Investigate` ก่อน `Delete`

---

## Step 7 — ตรวจ Data Type และ Date (7 นาที)
ตรวจว่า:
- Date เป็น Date จริง ไม่ใช่ text
- Sales/Cost/Profit เป็น Number
- Discount เป็น Number/Percentage ที่สอดคล้องกัน

ลอง Sort Date จากเก่า→ใหม่ หาก Sort แปลก อาจเป็น text

---

## Step 8 — สร้าง Data Quality Log (10 นาที)
สร้าง Tab ใหม่ชื่อ `Data_Quality_Log`

ใช้โครงสร้าง:

| # | Issue Type | Field/Row | Evidence | Decision | Reason |
|---|---|---|---|---|---|
| 1 | Category | Region | `south`, ` SOUTH ` | Standardize | หมายถึง Region เดียวกัน |
| 2 | Missing | Sales | blank record | Flag | ไม่มีข้อมูลพอให้เติมค่า |
| 3 | Impossible | Discount | 2.50 | Investigate | เกินช่วงปกติอย่างมาก |

**ต้องมีอย่างน้อย 5 issues**

---

## Step 9 — ให้ Copilot เป็น Reviewer หลังตรวจเอง (5 นาที)
หลังจากคุณมี Data Quality Log แล้ว จึงถาม Copilot:

```text
I checked this retail dataset for missing values, duplicates,
category inconsistencies, impossible values, and data types.
Suggest additional data-quality checks I may have missed.
Do not clean or modify the data for me.
```

จากคำตอบ AI ให้เลือก:
- 1 ข้อที่มีประโยชน์
- 1 ข้อที่ไม่จำเป็น/ใช้ไม่ได้กับ Dataset นี้

---

# Stop & Share — รอผู้สอน
เตรียมตอบ:

> Issue ใดที่ “ดูผิดปกติ” แต่คุณยังไม่ควรแก้ทันที และเพราะอะไร?

---

# สิ่งที่ต้องส่ง
1. Tab `Working_Data`
2. Tab `Data_Quality_Log`
3. Quality issues ≥5
4. Reflection 2 บรรทัด:
   - AI ช่วยเตือนอะไรที่ฉันพลาด?
   - ข้อเสนอ AI ข้อใดที่ฉันไม่ทำตาม?

---

# Core / Challenge

## Core
ตรวจ Missing, Duplicate, Category, Impossible Value, Type

## Challenge
สร้าง `Quality_Check` column เพื่อ Flag row ที่ต้องตรวจเพิ่ม เช่น:

```text
=IF(OR(G2<0,H2>1,I2="",K2=""),"CHECK","OK")
```

ปรับ column reference ให้ตรงกับไฟล์จริง

---

# Common Mistakes
- แก้ Raw Data โดยไม่มีสำเนา
- ลบ Outlier ทันที
- เติม Missing ด้วยค่าเฉลี่ยโดยไม่ถาม Business Meaning
- เชื่อ AI ว่าค่าใด “ผิด” โดยไม่ตรวจหน่วย/บริบท

**จำไว้:** Data Cleaning คือการตัดสินใจที่ต้องมีเหตุผล ไม่ใช่แค่ทำให้ตารางดูสะอาด
