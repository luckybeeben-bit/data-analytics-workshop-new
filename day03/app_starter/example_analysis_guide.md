# ตัวอย่างขั้นตอนวิเคราะห์ข้อมูลและเลือกกราฟ

ใช้คู่กับ `example_analysis.py` ซึ่งรันได้ครบตั้งแต่อ่าน CSV ถึงส่งออกผล ไม่ต้องคัดลอกโค้ดทีละส่วน ตัวอย่างนี้ใช้ข้อมูลเดียวกับ `example_app.py` เพื่อให้ตรวจที่มาของข้อเสนอได้ ส่วนกราฟเส้นใช้ข้อมูล Marketing Day 2 เพราะมีคอลัมน์เดือนจริง

## วิธีรันและเปิดผล

จาก repository root ใน environment ที่ติดตั้ง `requirements.txt` แล้ว:

```bash
python day03/app_starter/example_analysis.py
```

หากใช้ `.venv` บน Windows โดยยังไม่ได้ activate:

```powershell
.\.venv\Scripts\python.exe day03/app_starter/example_analysis.py
```

ผลอยู่ใน `day03/output/example_analysis/` มีตาราง CSV 10 ไฟล์ กราฟ HTML 8 ไฟล์ และ `index.html` สำหรับเลือกเปิดกราฟ เก็บ `plotly.min.js` ไว้ในโฟลเดอร์เดียวกันเพื่อเปิดกราฟแบบออฟไลน์ หากจะแชร์ให้ส่งทั้งโฟลเดอร์ ผลที่สร้างใหม่ถูกแยกออกจาก Git และสร้างซ้ำได้ด้วยคำสั่งเดิม

กำหนดตำแหน่งผลลัพธ์เองได้ด้วย `--output-dir path/to/output` การรันซ้ำจะเขียนทับไฟล์ผลลัพธ์ชื่อเดิมในโฟลเดอร์นั้น

## ขั้นที่ 1 — ตั้งคำถามและรู้จักข้อมูล

คำถามคือ “ควรเริ่มตรวจและทดลองปรับปรุงบริการ 3 สาขาใด?” ตัวชี้วัดหลักจึงเป็นอัตราร้องเรียนและเวลาบริการ ส่วนรายได้/กำไรบอกขนาดธุรกิจ และ Rating/Repeat Purchase ใช้ดูผลลัพธ์ด้านลูกค้า

หากต้องการทดลองใน Python console หรือ notebook จาก repository root ให้รันชุดเตรียมนี้ก่อน ตัวอย่างโค้ดด้านล่างใช้ตัวแปรเหล่านี้ร่วมกัน:

```python
import pandas as pd
import plotly.express as px
from day03.app_starter.example_analysis import (
    load_branch_data, analyze_branches, monthly_marketing, build_charts,
)

df, profile, duplicate_count = load_branch_data()
tables = analyze_branches(df)
summary = tables["branch_summary"]
segment = tables["branch_segment"]
monthly = monthly_marketing()

print(df.head())
df.info()
print(df.describe())
print(df["Customer_Segment"].value_counts(dropna=False))
```

หนึ่งแถวมี Branch และ Customer_Segment พร้อมยอด/อัตราหลายตัว แต่ไฟล์ไม่ได้บอกวันที่หรือรหัสรายการ จึงอย่าสมมติว่า 1 แถว = ลูกค้า 1 คน หรือธุรกรรม 1 ครั้ง การรู้หน่วยข้อมูลสำคัญก่อนรวมยอดและตีความการกระจาย

## ขั้นที่ 2 — ตรวจคุณภาพและเตรียมข้อมูล

```python
print(profile)  # dtype เดิมและจำนวน missing ก่อน/หลังแปลง
print("Exact duplicate rows:", duplicate_count)

# ตัวอย่างวิธีที่อยู่ภายใน load_branch_data():
converted = pd.to_numeric(df["Complaint_Rate"], errors="coerce")
invalid_rate = converted.isna() | ~converted.between(0, 1)
print(df.loc[invalid_rate])
```

`errors="coerce"` เปลี่ยนค่าที่แปลงไม่ได้เป็น missing เพื่อให้ตรวจเจอ ไม่ใช่อนุญาตให้ทิ้งแถวนั้นแล้ววิเคราะห์ต่อ สคริปต์หยุดเมื่อพบค่าที่จำเป็นหาย ตัวเลขอนันต์ ค่าติดลบในฟิลด์ที่ไม่ควรติดลบ หรืออัตรานอก 0–1 โดยสมมติ Rating สเกล 0–5

แถวที่ทุกคอลัมน์เหมือนกันเป็นสัญญาณให้ตรวจซ้ำ ไม่ใช่หลักฐานว่าเป็นรายการบันทึกซ้ำ จึงไม่ใช้ `drop_duplicates()` โดยอัตโนมัติ และกำไรติดลบยังเป็นค่าที่เป็นไปได้

## ขั้นที่ 3 — สรุปด้วย groupby และสร้างตัวชี้วัด

```python
example_summary = df.groupby("Branch", as_index=False).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Complaint_Rate=("Complaint_Rate", "mean"),
    Service_Time_Min=("Service_Time_Min", "mean"),
    Rows=("Branch", "size"),
)
example_summary["Profit_Margin"] = example_summary["Profit"].div(
    example_summary["Revenue"].where(example_summary["Revenue"].ne(0))
)
print(example_summary)
```

`sum` รวมยอด ส่วน `mean` เฉลี่ยค่าแต่ละแถวด้วยน้ำหนักเท่ากันตามข้อตกลง workshop `Profit_Margin` ต้องคำนวณจาก **กำไรรวม / รายได้รวม** ไม่ใช่เฉลี่ย Margin รายแถว ถ้ารายได้เป็นศูนย์จะให้ missing เพราะอัตรานี้ไม่มีนิยาม แทนการใส่ 0 แล้วสื่อว่ารู้ค่า

อัตราร้องเรียนในข้อมูลนี้ไม่มีจำนวนร้องเรียนและตัวหารจริง จึงยังคำนวณอัตรารวมที่ถ่วงตามฐานลูกค้าไม่ได้ และ `Orders` ไม่ใช่ตัวหารที่ใช้กับทุกอัตราได้โดยอัตโนมัติ

## ขั้นที่ 4 — กรอง จัดอันดับ และเปรียบเทียบ

```python
above_median = summary.loc[
    summary["Complaint_Rate"].gt(summary["Complaint_Rate"].median())
    & summary["Service_Time_Min"].gt(summary["Service_Time_Min"].median())
]
ranking = summary.sort_values(
    ["Complaint_Rate", "Service_Time_Min", "Branch"],
    ascending=[False, False, True],
)
print(ranking.head(3))
print(tables["group_comparison"])
print(tables["rank_sensitivity"])
```

การกรอง “สูงกว่า median ทั้งสองตัว” กับ “3 อันดับตามร้องเรียน” เป็นคนละเกณฑ์และอาจได้คนละชุด Median เป็น benchmark ภายในข้อมูล ไม่ใช่ระดับบริการที่ยอมรับได้ตามข้อตกลงธุรกิจ

ใน ranking นี้ Service Time ใช้ตัดสินเมื่อ Complaint เท่ากันเท่านั้น ตาราง `rank_sensitivity` ให้ลองเปลี่ยนไปจัดลำดับด้วยเวลาให้บริการหรือรายได้ แล้วดูว่าข้อเสนอไวต่อเกณฑ์เพียงใด การเลือกเกณฑ์เป็นการตัดสินใจของผู้วิเคราะห์ ไม่ใช่ข้อเท็จจริงที่ข้อมูลเลือกให้

## ขั้นที่ 5 — แยก Segment เพื่อไม่ให้ค่าเฉลี่ยบังรายละเอียด

```python
print(segment)
matrix = segment.pivot(
    index="Branch", columns="Customer_Segment", values="Complaint_Rate"
)
print(matrix)
print(segment.groupby("Branch")["Row_Share"].sum())  # ควรเป็น 1 ทุกสาขา
```

ตรวจว่าปัญหาปรากฏในหลาย Segment หรือกระจุกในบางกลุ่ม และดูจำนวนแถวประกอบ หากสัดส่วน Segment ต่างกัน ค่าเฉลี่ยรวมอาจเทียบกันได้ไม่ตรงนัก ตารางนี้ช่วยสำรวจ แต่ยังไม่ใช่การควบคุมความต่างของกลุ่มลูกค้าทางสถิติ ช่องที่ไม่มีข้อมูลต้องเป็น missing ไม่เติม 0 และ `Row_Share` เป็นสัดส่วนแถว ไม่ใช่สัดส่วนลูกค้า

## ขั้นที่ 6 — ตรวจความสัมพันธ์โดยไม่สรุปสาเหตุ

```python
correlation = summary[
    ["Complaint_Rate", "Service_Time_Min", "Rating", "Repeat_Purchase_Rate"]
].corr(method="spearman")
print(correlation)
```

Spearman วัดความสัมพันธ์ของอันดับ ค่าใกล้ +1 หมายถึงอันดับมีแนวโน้มไปทางเดียวกัน ใกล้ −1 สวนทางกัน ค่าใกล้ 0 หมายถึงไม่มีความสัมพันธ์แบบ monotonic ชัดเจน ไม่ได้แปลว่าไม่มีความสัมพันธ์ทุกแบบ ตัวแปรคงที่จะให้ค่า correlation ที่ไม่มีนิยามได้

ที่นี่ใช้ค่าเฉลี่ยรายสาขา จึงมีหน่วยวิเคราะห์เป็นสาขา ไม่ใช่ลูกค้า ความสัมพันธ์จากสาขาจำนวนน้อยนี้ยังไม่พิสูจน์เหตุและผล และนำไปอ้างพฤติกรรมลูกค้าแต่ละคนโดยตรงไม่ได้

## ขั้นที่ 7 — ตัวอย่างสร้างกราฟ 8 แนวทาง

ตัวอย่างสั้นด้านล่างเรียก `fig.show()` เพื่อเปิดกราฟระหว่างทดลอง ใน Streamlit เปลี่ยนเป็น `st.plotly_chart(fig, width="stretch")` สคริปต์เต็มใช้ `build_charts()` แล้วส่งออก HTML ให้เปิดตรวจได้ทุกแบบ

| แบบ | คำถามที่เหมาะ | ข้อมูลที่ใช้ | จุดระวัง |
|---|---|---|---|
| A. Ranked bar | สาขาใดมีค่าสูงสุด? | ค่าเฉลี่ยรายสาขา | แกนค่าควรเริ่ม 0 |
| B. Grouped bar | รายได้กับกำไรต่างกันอย่างไร? | ยอดรวมรายสาขา | ไม่ใช้ stacked เพราะกำไรอยู่ภายในรายได้ |
| C. Bubble scatter | ตัวแปรสองตัวเกิดร่วมกันหรือไม่? | รายสาขา | ความสัมพันธ์ไม่ใช่สาเหตุ |
| D. Histogram | ค่าส่วนใหญ่อยู่ช่วงใด? | แถวต้นทาง | รูปร่างเปลี่ยนได้ตามจำนวน bins |
| E. Box plot | ค่าภายในแต่ละสาขากระจายแค่ไหน? | แถวต้นทาง | outlier ไม่ได้แปลว่าข้อมูลผิด |
| F. Heatmap | Branch × Segment กลุ่มใดค่าสูง? | ค่าเฉลี่ยสองมิติ | missing ไม่ใช่ 0; ตรวจ Rows ด้วย |
| G. 100% stacked bar | ส่วนประกอบ Segment ต่างกันไหม? | สัดส่วนแถวรายสาขา | ไม่แสดงขนาดรวมและไม่ใช่จำนวนลูกค้า |
| H. Line | ผลลัพธ์เปลี่ยนตามเวลาอย่างไร? | Marketing รายเดือน | ต้องมีวันที่จริงและเรียงเวลา |

### A. แท่งแนวนอนเรียงอันดับ

```python
ordered = summary.sort_values("Complaint_Rate", ascending=False)
fig = px.bar(ordered, x="Complaint_Rate", y="Branch", orientation="h",
             category_orders={"Branch": ordered["Branch"].tolist()})
fig.update_xaxes(tickformat=".1%", rangemode="tozero")
fig.show()
```

### B. แท่งเปรียบเทียบด้วยข้อมูลแบบ long

```python
long_data = summary.melt(id_vars="Branch", value_vars=["Revenue", "Profit"],
                         var_name="Metric", value_name="Amount")
fig = px.bar(long_data, x="Branch", y="Amount", color="Metric", barmode="group")
fig.update_yaxes(rangemode="tozero")
fig.show()
```

`melt` เปลี่ยนคอลัมน์ตัวชี้วัดให้เป็นแถว ทำให้ Plotly ใช้สีแยก Metric ได้ หากสเกลต่างกันมาก ใช้ `facet_col="Metric"` แยกพื้นที่วาด แต่ต้องระบุสเกลให้ชัดเมื่อจะเทียบขนาด

### C. Bubble scatter

```python
fig = px.scatter(summary, x="Service_Time_Min", y="Complaint_Rate",
                 size="Revenue", color="Group", hover_name="Branch")
fig.update_yaxes(tickformat=".1%")
fig.show()
```

### D. Histogram

```python
fig = px.histogram(df, x="Service_Time_Min", nbins=20)
fig.update_yaxes(title_text="Number of source rows")
fig.show()
```

ลอง `nbins=10` และ `nbins=30` เพื่อดูว่าข้อสังเกตยังเหมือนเดิมหรือไม่ ค่าที่นำมาวาดเป็นเวลาบริการระดับแถวตามไฟล์ ไม่สามารถอ้างว่าเป็นการกระจายเวลารอของลูกค้าทุกรายได้

### E. Box plot

```python
fig = px.box(df, x="Branch", y="Service_Time_Min", points="outliers")
fig.show()
```

เส้นในกล่องแสดง median กล่องครอบคลุม Q1–Q3 จุดนอก whisker ตามเกณฑ์ของ box plot ใช้ชี้แถวที่ควรตรวจเพิ่มเติม ก่อนสรุปว่าสาขาที่มีค่าเฉลี่ยเท่ากันมีความสม่ำเสมอเหมือนกัน ให้ดูการกระจายด้วย

### F. Heatmap

```python
matrix = segment.pivot(index="Branch", columns="Customer_Segment", values="Complaint_Rate")
fig = px.imshow(matrix, text_auto=".1%", aspect="auto", zmin=0,
                color_continuous_scale="Oranges")
fig.update_layout(coloraxis_colorbar_tickformat=".1%")
fig.show()
```

### G. แท่งสัดส่วนรวม 100%

```python
fig = px.bar(segment, x="Branch", y="Row_Share", color="Customer_Segment",
             barmode="stack", hover_data=["Rows"])
fig.update_yaxes(tickformat=".0%", range=[0, 1])
fig.show()
```

### H. กราฟเส้นตามเดือนจริงจาก Day 2

```python
monthly = monthly_marketing()
fig = px.line(monthly.sort_values(["Channel", "Month"]),
              x="Month", y="ROAS", color="Channel", markers=True)
fig.update_traces(connectgaps=False)
fig.show()
```

ฟังก์ชันแปลง `Month` เป็นวันแรกของเดือน รวม Revenue และ Spend ต่อเดือน/Channel แล้วคำนวณ `ROAS = Revenue รวม / Spend รวม` ไม่เฉลี่ย ROAS รายแถว และเติมช่องเดือนที่หายเป็น missing เพื่อให้เส้นขาด ไม่สร้างภาพว่ามีข้อมูลต่อเนื่อง รายได้เทียบค่าโฆษณายังไม่ใช่กำไรหรือผลตอบแทนสุทธิของธุรกิจ

## ขั้นที่ 8 — บันทึกผลและตรวจย้อนกลับ

```python
from pathlib import Path

output = Path("day03/output/example_analysis")
output.mkdir(parents=True, exist_ok=True)
summary.to_csv(output / "branch_summary.csv", index=False, encoding="utf-8-sig")
charts = build_charts(df, tables, monthly)
charts["01_ranked_bar"].write_html(output / "ranking_demo.html")
```

ตรวจยอด Revenue/Profit ก่อนและหลัง groupby ว่าตรงกัน ตรวจว่า `Row_Share` รวมได้ 1 ต่อสาขา และชื่อ 3 สาขาแรกตรงกับแอป หากค่าที่อ่านจากกราฟดูแปลก ให้กลับมาตรวจตารางก่อนเขียน Insight

## Prompt สำหรับฝึกขยายตัวอย่าง

```text
อ่าน example_analysis.py และข้อมูลจริงก่อนแก้โค้ด
เพิ่มการวิเคราะห์ [ระบุคำถาม] โดยระบุหน่วยข้อมูลและ aggregation
แสดงตารางหลักฐานก่อนเลือกกราฟ [ระบุชนิดกราฟหรือให้เสนอพร้อมเหตุผล]
อธิบาย input -> transformation -> output -> ความหมายต่อการตัดสินใจ
อย่า hard-code ผลลัพธ์ อย่าทิ้ง missing หรือเติม 0 โดยไม่อธิบาย
แยกข้อเท็จจริง สมมติฐาน และสิ่งที่ยังพิสูจน์ไม่ได้
ส่งออกตารางและกราฟที่รันซ้ำได้ พร้อมวิธีตรวจว่าผลคำนวณถูกต้อง
```

เลือกกราฟเพียง 2–4 แบบที่ตอบคำถามต่างกันไปใช้ในหน้าผู้บริหาร ส่วนตัวอย่างทั้ง 8 แบบนี้ใช้สำหรับเรียนรู้และสำรวจข้อมูล
