import pandas as pd

DATA_PATH = "day02/case02_marketing/data/marketing_performance.csv"
df = pd.read_csv(DATA_PATH)

print(df.head())
print(df.info())

business_question = "Which channels and customer segments deserve more or less budget?"

# TODO 1: Data quality checks
# TODO 2: Compare Spend / Revenue / Conversion Rate / ROAS by Channel
# TODO 3: Compare by Customer_Segment
# TODO 4: Identify trade-offs rather than optimizing one metric
# TODO 5: Write evidence in day02/output/evidence.md
