# LAB 06 — AI Verification Challenge: ใช้ Copilot แต่ห้ามยก Decision ให้ AI
**Day 2 | ANALYZE & INTERPRET**  
**เวลา:** 75 นาที | **รูปแบบ:** Individual | **เครื่องมือ:** GitHub Copilot + Python/Pandas

## เป้าหมายของ Lab
ฝึกใช้ Copilot เป็น **Question Coach / Coding Assistant / Reviewer** โดยผู้เรียนยังคงเป็นคนเลือกวิธีวิเคราะห์ ตรวจ Code และตัดสินว่า Claim ใดมี Evidence รองรับจริง

Learning loop:

> **Predict → Ask AI → Inspect → Run → Explain → Verify → Decide**

---

# ขั้นตอนการทดลอง

## Step 1 — Predict ก่อนเปิด Copilot (7 นาที)
ปิด/ยังไม่ใช้ Chat ก่อน

เขียนเอง:

```text
Business Question:
Which channels and customer segments deserve more or less budget?

My analysis plan (3 items):
1. __________________________________
2. __________________________________
3. __________________________________
```

สำหรับแต่ละข้อ เขียนว่าคาดว่าจะใช้ Metric อะไร

### จุดประสงค์
ต้องมี “ความคิดของคุณ” ก่อนเห็นคำตอบ AI เพื่อป้องกัน anchoring

---

## Step 2 — Ask AI เฉพาะแผนก่อน ยังไม่ขอ Code (8 นาที)
เปิด Copilot Chat และใช้ Prompt:

```text
I am analyzing a marketing dataset to support budget allocation.
My current analysis plan is:
1. ...
2. ...
3. ...

Suggest up to three analyses I may have missed.
Do not write code yet.
For each suggestion, explain which business question it helps answer.
```

สร้างตาราง:

| AI Suggestion | Keep / Reject | Why? |
|---|---|---|
| | | |

ต้อง **Reject อย่างน้อย 1 ข้อ** ถ้ามีข้อที่ไม่จำเป็น/ไม่ตอบ Decision

---

## Step 3 — เลือก Analysis เพียง 1 ชิ้นให้ AI ช่วย Implement (10 นาที)
ใช้ Prompt:

```text
Help me implement only analysis #__ using pandas.
Use the existing dataframe `df`.
Keep the code simple.
Before giving the code, explain:
1. input columns
2. transformation
3. expected output
4. why it helps the budget decision
```

### ก่อน Run
เขียน Prediction:

```text
I expect this code to output:
____________________________________
```

---

## Step 4 — Inspect Code ทีละ block (10 นาที)
ก่อนกด Run ให้ตรวจ:
- Column มีจริงหรือไม่?
- Aggregation เหมาะไหม (`sum` vs `mean`)?
- Filter ตรงโจทย์ไหม?
- Ratio คำนวณถูกฐานไหม?
- AI hard-code ตัวเลข/ข้อสรุปไว้หรือไม่?

### Red Flag
Code แบบนี้ต้องระวัง:

```python
best_channel = "Email"  # hard-coded conclusion
```

Decision ต้องมาจาก data ไม่ใช่ AI เขียนชื่อคำตอบใส่ code

---

## Step 5 — Run และเปรียบเทียบกับ Prediction (8 นาที)
Run code

บันทึก:

```text
Expected:
Actual:
Difference:
```

ถ้าผลต่างจากที่คาด ให้หาสาเหตุก่อนถาม AI รอบใหม่

---

## Step 6 — Explain Back: อธิบาย Code ด้วยภาษาของตนเอง (8 นาที)
ห้าม copy คำอธิบาย AI

ใช้ template:

> Code นี้เริ่มจาก ______ จากนั้น group/filter ด้วย ______ แล้วคำนวณ ______ ผลลัพธ์ช่วยให้เราเปรียบเทียบ ______

ผู้สอนอาจสุ่มให้พูด 30 วินาที

---

## Step 7 — ให้ AI Review Interpretation ไม่ใช่สร้าง Conclusion ใหม่ (8 นาที)
เขียน Interpretation ของคุณก่อน 2–3 ประโยค แล้วใช้ Prompt:

```text
Review my interpretation below.
Separate each statement into:
- Evidence
- Interpretation
- Hypothesis
- Recommendation

Identify any claim that is not directly supported by the dataframe output.
Do not rewrite the final recommendation for me.

My interpretation:
...
```

---

## Step 8 — ตรวจ Claim กลับไปที่ Output จริง (8 นาที)
ทุก Claim ที่ AI บอกว่าเป็น Evidence ต้องตอบได้ว่า:

- มาจาก dataframe/table ไหน?
- Filter อะไร?
- Metric อะไร?
- Comparison กับอะไร?

ถ้าตอบไม่ได้ → Claim นั้นยังไม่ควรถูกใช้

---

## Step 9 — เขียน “I disagree with AI” อย่างน้อย 1 จุด (4 นาที)

```text
I disagree with / did not use AI suggestion ______
because ___________________________________________.
```

ถ้าคุณเห็นด้วยกับ AI ทุกอย่าง ให้กลับไปตรวจว่าได้ Review จริงหรือไม่

---

## Step 10 — Commit งาน (4 นาที)
ตรวจ `git status`

```bash
git status
```

จากนั้น:

```bash
git add .
git commit -m "Complete Lab06 AI verification"
```

> ถ้า workshop ใช้ repository แบบ read-only/master ให้ทำตาม workflow ที่ผู้สอนกำหนดแทน

---

# สิ่งที่ต้องส่ง
1. Analysis plan ก่อน AI
2. AI suggestions + Keep/Reject
3. Code ที่ Run ได้
4. Evidence 3–5 ข้อ
5. Hypothesis ≥1
6. `I disagree with AI...` ≥1
7. คำอธิบาย Code ด้วยภาษาตนเอง 1 block

---

# Core / Challenge

## Core
ทำวงจร Predict → Ask → Verify ให้ครบ 1 analysis

## Challenge
ให้ Copilot Review code จากมุม **robustness** เช่น ratio weighting, missing values, sample size แต่ห้ามให้เปลี่ยน business conclusion อัตโนมัติ

---

# Common Mistakes
- ขอ AI ว่า “วิเคราะห์ dataset แล้วบอกว่าควรทำอะไร” ตั้งแต่แรก
- Run code ก่อนอ่าน
- ยอมรับ causal claim ของ AI
- ไม่ย้อน Claim กลับไปหา table/output

**จำไว้:** AI ช่วยลดเวลา Implement แต่ไม่ได้ลดความรับผิดชอบในการ Verify
