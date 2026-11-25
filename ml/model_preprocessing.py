import joblib
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

# Load dataset
df = pd.read_excel("dataset/Risk_data.xlsx")

# Remove Project ID
df = df.drop(columns=["Project ID"])

# Separate input features and target variables
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

# Identify categorical and numerical columns
categorical_features = ["Project Industry"]

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y["Risk Type"]
)

# Pipeline for Random Forest and XGBoost
tree_preprocessor = ColumnTransformer(
    transformers=[
        ("categorical",
         OneHotEncoder(handle_unknown="ignore"),
         categorical_features)
    ],
    remainder="passthrough"
)

# Pipeline for Logistic Regression and SVM
scaled_preprocessor = ColumnTransformer(
    transformers=[
        ("categorical",
         OneHotEncoder(handle_unknown="ignore"),
         categorical_features),
        ("numerical",
         StandardScaler(),
         numerical_features)
    ]
)

# Fit only on training data
X_train_tree = tree_preprocessor.fit_transform(X_train)
X_test_tree = tree_preprocessor.transform(X_test)

X_train_scaled = scaled_preprocessor.fit_transform(X_train)
X_test_scaled = scaled_preprocessor.transform(X_test)

# Display results
print("ENCODING AND SCALING COMPLETED!")

print("\nOriginal Training Features:", X_train.shape)

print("\nTree Model Features:")
print("Training:", X_train_tree.shape)
print("Testing:", X_test_tree.shape)

print("\nScaled Model Features:")
print("Training:", X_train_scaled.shape)
print("Testing:", X_test_scaled.shape)

print("\nCategorical Columns:", categorical_features)
print("Numerical Columns:", len(numerical_features))

# Save preprocessing objects
os.makedirs("models", exist_ok=True)

joblib.dump(
    tree_preprocessor,
    "models/tree_preprocessor.pkl"
)

joblib.dump(
    scaled_preprocessor,
    "models/scaled_preprocessor.pkl"
)

print("\nPreprocessing objects saved successfully!")