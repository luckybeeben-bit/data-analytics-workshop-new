# Data Analytics for Business Decision & Action — Instructor Pack

หลักสูตรอบรม 4 วัน สำหรับผู้เข้าอบรมที่ต้องการ upskill ทางด้าน Data Analytics

**Business Problem → Analytical Question → Data → Analysis → Evidence → Insight → Recommendation → Action Plan → Executive Communication**

## Tool Stack
Google Sheets → GitHub/Codespaces → VS Code → GitHub Copilot → Python/Pandas → Plotly/Streamlit

## Learning Rule
**Predict → Ask AI → Inspect → Run → Explain → Verify → Decide**

## Folder Map
- `day01/` Question & Evidence
- `day02/` Analyze & Interpret
- `day03/` Communicate & Decide
- `capstone/` Recommend & Act
- `assessment/` Pre/Post-test และ Rubric

## Workflow สำหรับผู้เข้าอบรม

ไปที่ link : https://github.com/anant/data-analytics-workshop
login github ด้วย gmail
พร้อมคำสั่ง:
### Step 1 : กดปุ่ม Use this template สีเขียวที่มุมขวาบน
### Step 2 : เลือก Create a new repository
    ตั้งชื่อ เช่น data-analytics-workshop-yourname
### Step 3 : เข้า repository ของตัวเอง
### Step 4 : เลือก
Code → Codespaces → Create codespace on main
GitHub จะสร้าง VM/container และ clone repository เข้า Codespace ให้โดยอัตโนมัติ ดังนั้นครั้งแรกผู้เรียน ไม่ต้อง git pull เอง
ถ้า .devcontainer/devcontainer.json ของเราพร้อมอยู่แล้ว จะติดตั้ง Python extensions, Copilot extensions, packages และ forward Streamlit port ตามที่เราเตรียมไว้

# Learner Quick Start
## 1) เปิด Codespaces
1. Login GitHub
2. เปิด repository ของหลักสูตร
3. กด Code → Codespaces → Create codespace
4. รอ setup เสร็จ
## 2) ตรวจ Python packages
```bash
python -c "import pandas, streamlit, plotly; print('READY')"
```
## 3) Run Day 2 Starter
```bash
python day02/starter/analysis_starter.py
```
## 4) Run Day 3 Streamlit App
```bash
streamlit run day03/app_starter/app.py
```
## 5) ใช้ Copilot อย่างถูกต้อง
ใช้วงจร:
**Predict → Ask AI → Inspect → Run → Explain → Verify → Decide**

ห้ามใช้ AI เพื่อสร้างข้อสรุปแทนโดยไม่ตรวจ Evidence
