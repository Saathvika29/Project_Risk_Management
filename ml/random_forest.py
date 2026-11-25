
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)

# 1. Load dataset
df = pd.read_excel("dataset/Risk_data.xlsx")

# 2. Remove Project ID
df = df.drop(columns=["Project ID"])

# 3. Separate features and targets
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

# 4. Identify feature types
categorical_features = ["Project Industry"]

# 5. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y["Risk Type"]
)

# 6. Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# 7. Create models directory
os.makedirs("models", exist_ok=True)

# 8. Define target types
classification_targets = [
    "Risk Type",
    "Risk Response Plan"
]

regression_targets = [
    "Risk Impact",
    "Risk Probability"
]

# 9. Train classification models
for target in classification_targets:

    print("\n" + "=" * 50)
    print("RANDOM FOREST CLASSIFICATION:", target)
    print("=" * 50)

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    model.fit(X_train, y_train[target])

    predictions = model.predict(X_test)

    print("\nAccuracy:",
          accuracy_score(y_test[target], predictions))

    print("Macro F1 Score:",
          f1_score(y_test[target], predictions, average="macro"))

    print("Balanced Accuracy:",
          balanced_accuracy_score(y_test[target], predictions))

    print("\nClassification Report:")
    print(classification_report(
        y_test[target],
        predictions,
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test[target], predictions))

    joblib.dump(model, f"models/random_forest_{target.lower().replace(' ', '_')}.pkl")


# 10. Train regression models
for target in regression_targets:

    print("\n" + "=" * 50)
    print("RANDOM FOREST REGRESSION:", target)
    print("=" * 50)

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train[target])

    predictions = model.predict(X_test)

    print("\nMean Absolute Error:",
          mean_absolute_error(y_test[target], predictions))

    print("Root Mean Squared Error:",
          root_mean_squared_error(y_test[target], predictions))

    print("R2 Score:",
          r2_score(y_test[target], predictions))

    joblib.dump(model, f"models/random_forest_{target.lower().replace(' ', '_')}.pkl")

print("\n" + "=" * 50)
print("ALL RANDOM FOREST MODELS TRAINED SUCCESSFULLY!")
print("Models saved inside the models folder.")
print("=" * 50)
