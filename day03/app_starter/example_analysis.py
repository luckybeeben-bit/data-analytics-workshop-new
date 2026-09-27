"""ตัวอย่างวิเคราะห์ทีละขั้นและกราฟ 8 แนวทาง (ดู example_analysis_guide.md).

Run from repository root: python day03/app_starter/example_analysis.py
Output: day03/output/example_analysis/ (CSV tables + offline HTML charts)
"""

import argparse
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
BRANCH_PATH = ROOT / "day03/case03_branch/data/branch_customer_performance.csv"
MARKETING_PATH = ROOT / "day02/case02_marketing/data/marketing_performance.csv"
NUMERIC = [
    "Orders", "Revenue", "Profit", "Rating", "Repeat_Purchase_Rate",
    "Complaint_Rate", "Service_Time_Min",
]


def load_branch_data(path=BRANCH_PATH):
    """1–2: อ่าน ตรวจ และแปลงชนิดข้อมูล โดยไม่ทิ้งแถวเสียเงียบ ๆ."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    required = ["Branch", "Customer_Segment", *NUMERIC]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("The dataset is empty.")

    profile = pd.DataFrame({
        "Column": required,
        "Original_Dtype": [str(df[c].dtype) for c in required],
        "Missing_Before": [df[c].isna().sum() for c in required],
    })
    df[NUMERIC] = df[NUMERIC].apply(pd.to_numeric, errors="coerce")
    for col in ["Branch", "Customer_Segment"]:
        df[col] = df[col].astype("string").str.strip().replace("", pd.NA)
    profile["Missing_After"] = [df[c].isna().sum() for c in required]
    invalid = (
        df[required].isna().any(axis=1)
        | df[NUMERIC].isin([float("inf"), float("-inf")]).any(axis=1)
        | df[["Orders", "Revenue", "Service_Time_Min"]].lt(0).any(axis=1)
        | ~df["Rating"].between(0, 5)
        | ~df["Repeat_Purchase_Rate"].between(0, 1)
        | ~df["Complaint_Rate"].between(0, 1)
    )
    if invalid.any():
        raise ValueError(f"Invalid rows (zero-based index): {df.index[invalid].tolist()[:10]}")
    # แถวเหมือนกันไม่จำเป็นต้องเป็นรายการซ้ำ จึงรายงานแต่ไม่ drop_duplicates()
    duplicate_count = int(df.duplicated().sum())
    return df, profile, duplicate_count


def analyze_branches(df):
    """3–6: สรุป กรอง เปรียบเทียบ แยก Segment และตรวจความไวของอันดับ."""
    summary = df.groupby("Branch", as_index=False).agg(
        Revenue=("Revenue", "sum"), Profit=("Profit", "sum"),
        Orders=("Orders", "sum"), Rows=("Branch", "size"),
        Rating=("Rating", "mean"),
        Repeat_Purchase_Rate=("Repeat_Purchase_Rate", "mean"),
        Complaint_Rate=("Complaint_Rate", "mean"),
        Service_Time_Min=("Service_Time_Min", "mean"),
    )
    # Ratio of totals: สาขารายได้ศูนย์ไม่มีนิยาม Margin จึงให้ missing ไม่ใส่ 0
    summary["Profit_Margin"] = summary["Profit"].div(summary["Revenue"].where(summary["Revenue"].ne(0)))
    ranking = summary.sort_values(
        ["Complaint_Rate", "Service_Time_Min", "Branch"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    if len(ranking) < 4:
        raise ValueError("Need at least 4 branches to compare the top 3 with peers.")
    ranking.insert(0, "Priority", range(1, len(ranking) + 1))
    selected_names = ranking.head(3)["Branch"]
    summary["Group"] = summary["Branch"].isin(selected_names).map(
        {True: "Selected", False: "Other"}
    )
    # Median เป็น benchmark ภายในชุดข้อมูล ไม่ใช่มาตรฐานคุณภาพบริการ
    above_median = summary.loc[
        summary["Complaint_Rate"].gt(summary["Complaint_Rate"].median())
        & summary["Service_Time_Min"].gt(summary["Service_Time_Min"].median())
    ].copy()
    comparison = summary.groupby("Group", as_index=False).agg(
        Branches=("Branch", "size"), Revenue=("Revenue", "sum"),
        Complaint_Rate=("Complaint_Rate", "mean"),
        Service_Time_Min=("Service_Time_Min", "mean"),
        Rating=("Rating", "mean"),
        Repeat_Purchase_Rate=("Repeat_Purchase_Rate", "mean"),
    )
    branch_segment = df.groupby(["Branch", "Customer_Segment"], as_index=False).agg(
        Rows=("Branch", "size"), Revenue=("Revenue", "sum"),
        Complaint_Rate=("Complaint_Rate", "mean"),
    )
    # จำนวนแถวใน Segment / จำนวนแถวสาขา ไม่ใช่สัดส่วนจำนวนลูกค้า
    branch_segment["Row_Share"] = branch_segment["Rows"].div(
        branch_segment.groupby("Branch")["Rows"].transform("sum")
    )
    sensitivity = ranking[["Branch", "Priority"]].copy()
    for metric in ["Service_Time_Min", "Revenue"]:
        alternative = summary.sort_values([metric, "Branch"], ascending=[False, True])
        positions = pd.Series(range(1, len(alternative) + 1), index=alternative["Branch"])
        sensitivity[f"Rank_by_{metric}"] = sensitivity["Branch"].map(positions)
    correlation_metrics = ["Complaint_Rate", "Service_Time_Min", "Rating", "Repeat_Purchase_Rate"]
    correlation = summary[correlation_metrics].corr(method="spearman")
    return {
        "branch_summary": summary,
        "ranking": ranking,
        "above_median": above_median,
        "group_comparison": comparison,
        "branch_segment": branch_segment,
        "rank_sensitivity": sensitivity,
        "spearman_correlation": correlation.rename_axis("Metric").reset_index(),
    }


def monthly_marketing(path=MARKETING_PATH):
    """กราฟเวลาใช้ Day 2 ที่มี Month จริง ไม่สมมติลำดับแถว Day 3 เป็นเวลา."""
    data = pd.read_csv(path, encoding="utf-8-sig")
    data["Month"] = pd.to_datetime(data["Month"], errors="raise").dt.to_period("M").dt.to_timestamp()
    for col in ["Spend", "Revenue"]:
        data[col] = pd.to_numeric(data[col], errors="raise")
    if (
        data.empty or data[["Month", "Channel", "Spend", "Revenue"]].isna().any().any()
        or data[["Spend", "Revenue"]].isin([float("inf"), float("-inf")]).any().any()
        or data["Spend"].lt(0).any()
    ):
        raise ValueError("Invalid monthly marketing data.")
    monthly = data.groupby(["Month", "Channel"], as_index=False).agg(
        Spend=("Spend", "sum"), Revenue=("Revenue", "sum"),
    )
    monthly["ROAS"] = monthly["Revenue"].div(monthly["Spend"].where(monthly["Spend"].ne(0)))
    # เติมเดือนที่ไม่มีข้อมูลเป็น missing เพื่อให้เส้นกราฟขาด ไม่ลากผ่านช่องว่าง
    complete_index = pd.MultiIndex.from_product(
        [pd.date_range(monthly["Month"].min(), monthly["Month"].max(), freq="MS"),
         sorted(monthly["Channel"].unique())], names=["Month", "Channel"],
    )
    return monthly.set_index(["Month", "Channel"]).reindex(complete_index).reset_index()


def build_charts(df, tables, monthly):
    """7: เลือกกราฟตามคำถาม ไม่จำเป็นต้องใช้ทุกกราฟบนหน้าผู้บริหาร."""
    summary = tables["branch_summary"]
    segment = tables["branch_segment"]
    order = tables["ranking"]["Branch"].tolist()
    colors = {"Selected": "#c2410c", "Other": "#64748b"}
    charts = {}

    # A. Ranking: แกนศูนย์ช่วยให้ความยาวแท่งเทียบกันได้ตรงไปตรงมา
    charts["01_ranked_bar"] = px.bar(
        summary, x="Complaint_Rate", y="Branch", orientation="h", color="Group",
        color_discrete_map=colors, category_orders={"Branch": order},
        title="A. Complaint rate ranking (row mean within each branch)",
    )
    charts["01_ranked_bar"].update_xaxes(tickformat=".1%", rangemode="tozero")

    # B. Grouped bar: melt เปลี่ยน wide -> long เพื่อเทียบตัวเลขสองชนิด
    business = summary.melt(id_vars="Branch", value_vars=["Revenue", "Profit"],
                            var_name="Metric", value_name="Amount")
    charts["02_grouped_bar"] = px.bar(
        business, x="Branch", y="Amount", color="Metric", barmode="group",
        category_orders={"Branch": order}, title="B. Revenue and profit context",
    )
    charts["02_grouped_bar"].update_yaxes(rangemode="tozero")

    # C. Bubble scatter: แต่ละจุดคือสาขา ขนาดคือรายได้ ไม่ใช่จำนวนร้องเรียน
    charts["03_bubble_scatter"] = px.scatter(
        summary, x="Service_Time_Min", y="Complaint_Rate", size="Revenue",
        color="Group", color_discrete_map=colors, hover_name="Branch",
        title="C. Service time vs complaints (association, not causation)",
    )
    charts["03_bubble_scatter"].update_yaxes(tickformat=".1%")

    # D. Histogram: ใช้แถวต้นทางเพื่อดูการกระจาย ไม่ใช่ค่าเฉลี่ยเพียง 12 สาขา
    charts["04_histogram"] = px.histogram(
        df, x="Service_Time_Min", nbins=20,
        title="D. Distribution of row-level service-time values",
        labels={"Service_Time_Min": "Service time (minutes)"},
    )
    charts["04_histogram"].update_yaxes(title_text="Number of source rows")

    # E. Box: จุดนอก whisker เป็นแถวที่ควรตรวจ ไม่ได้แปลว่าข้อมูลผิด
    charts["05_box_plot"] = px.box(
        df, x="Branch", y="Service_Time_Min", points="outliers",
        category_orders={"Branch": order}, title="E. Within-branch spread of row values",
    )

    # F. Heatmap: ช่องไม่มีข้อมูลคงเป็น NaN ไม่เติม 0 ซึ่งจะสื่อว่าร้องเรียนเป็นศูนย์
    matrix = segment.pivot(index="Branch", columns="Customer_Segment", values="Complaint_Rate")
    charts["06_segment_heatmap"] = px.imshow(
        matrix.reindex(order), text_auto=".1%", aspect="auto", zmin=0,
        color_continuous_scale="Oranges", title="F. Complaint rate by branch and segment",
        labels={"color": "Complaint rate"},
    )
    charts["06_segment_heatmap"].update_layout(coloraxis_colorbar_tickformat=".1%")

    # G. 100% stacked bar: ย้ำว่าฐานคือจำนวนแถว ไม่ใช่จำนวนลูกค้า
    charts["07_segment_mix"] = px.bar(
        segment, x="Branch", y="Row_Share", color="Customer_Segment",
        barmode="stack", hover_data=["Rows"], category_orders={"Branch": order},
        title="G. Segment composition of source rows (not customer share)",
    )
    charts["07_segment_mix"].update_yaxes(tickformat=".0%", range=[0, 1])

    # H. Line: sort เวลา, แยกเส้นตาม Channel, ไม่เฉลี่ย ROAS รายแถว
    charts["08_monthly_line"] = px.line(
        monthly.sort_values(["Channel", "Month"]), x="Month", y="ROAS", color="Channel",
        markers=True, title="H. Day 2 marketing ROAS over time (Revenue / Spend)",
        labels={"ROAS": "ROAS (times)"},
    )
    charts["08_monthly_line"].update_traces(connectgaps=False)
    return charts


def main():
    parser = argparse.ArgumentParser(description="Step-by-step analysis and 8 Plotly examples")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "day03/output/example_analysis")
    args = parser.parse_args()
    df, profile, duplicate_count = load_branch_data()
    tables = analyze_branches(df)
    monthly = monthly_marketing()
    tables.update({
        "data_quality": profile,
        "descriptive_statistics": df[NUMERIC].describe().rename_axis("Statistic").reset_index(),
        "monthly_marketing": monthly,
    })
    charts = build_charts(df, tables, monthly)

    # 8. ส่งออกเพื่อให้ผู้อื่นตรวจซ้ำได้; เปิด HTML ได้โดยไม่ต้องรัน server/ต่อ internet
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output / f"{name}.csv", index=False, encoding="utf-8-sig")
    links = []
    for name, figure in charts.items():
        figure.write_html(output / f"{name}.html", include_plotlyjs="directory", full_html=True)
        links.append(f'<li><a href="{name}.html">{escape(figure.layout.title.text)}</a></li>')
    (output / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Analysis examples</title>'
        '<body><h1>Analysis and chart examples</h1>'
        f'<p>Branch source rows: {len(df)}; exact duplicate rows: {duplicate_count}. '
        'Duplicates were reported, not removed.</p>'
        '<p>A–G: Day 3 branch data. H: Day 2 marketing data with actual months. '
        'Rates use equal row weights within branches; relationships do not establish causation.</p>'
        '<ol>' + ''.join(links) + '</ol></body></html>', encoding="utf-8",
    )
    print(f"Source rows: {len(df)}; exact duplicate rows: {duplicate_count} (not removed)")
    print(tables["ranking"][["Priority", "Branch", "Complaint_Rate", "Service_Time_Min"]].head(3).to_string(index=False))
    print(f"Saved {len(tables)} CSV tables and {len(charts)} HTML charts to {output}")
    print(f"Open {output / 'index.html'}")


if __name__ == "__main__":
    main()
