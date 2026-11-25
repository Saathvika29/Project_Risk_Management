
import pandas as pd

# Load the dataset
file_path = "dataset/Risk_data.xlsx"
df = pd.read_excel(file_path)

# 1. Dataset dimensions
print("\n========== DATASET SHAPE ==========")
print("Rows and Columns:", df.shape)

# 2. Column names
print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print(column)

# 3. Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# 4. Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 5. Duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print("Duplicates:", df.duplicated().sum())

# 6. Dataset information
print("\n========== DATASET INFO ==========")
df.info()

# 7. Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").T)

# 8. First five records
print("\n========== FIRST FIVE RECORDS ==========")
print(df.head())

# 9. Target variable distribution

targets = [
    "Risk Type",
    "Risk Impact",
    "Risk Probability",
    "Risk Response Plan"
]

print("\n========== TARGET DISTRIBUTION ==========")

for target in targets:
    print(f"\n--- {target} ---")
    print(df[target].value_counts())
    print("\nPercentage distribution:")
    print(df[target].value_counts(normalize=True) * 100)


# 10. Relationship between Risk Type and Risk Response Plan

print("\n========== RISK TYPE vs RESPONSE PLAN ==========")

relationship = pd.crosstab(
    df["Risk Type"],
    df["Risk Response Plan"]
)

print(relationship)

print("\nNumber of response plans for each risk type:")
print(df.groupby("Risk Type")["Risk Response Plan"].nunique())


