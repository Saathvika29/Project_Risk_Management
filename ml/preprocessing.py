
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load dataset
df = pd.read_excel("dataset/Risk_data.xlsx")

# 2. Remove Project ID (not useful for prediction)
df = df.drop(columns=["Project ID"])

# 3. Separate input features and target variables
X = df.drop(columns=[
    "Risk Type",
    "Risk Impact",
    "Risk Probability",
    "Risk Response Plan"
])

y = df[[
    "Risk Type",
    "Risk Impact",
    "Risk Probability",
    "Risk Response Plan"
]]

# 4. Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y["Risk Type"]
)

# 5. Display dataset information
print("DATA PREPROCESSING COMPLETED!")

print("\nOriginal Dataset:", df.shape)
print("Training Features:", X_train.shape)
print("Testing Features:", X_test.shape)

print("\nTraining Targets:", y_train.shape)
print("Testing Targets:", y_test.shape)

print("\nTraining Risk Type Distribution:")
print(y_train["Risk Type"].value_counts())

print("\nTesting Risk Type Distribution:")
print(y_test["Risk Type"].value_counts())
