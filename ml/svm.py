
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.svm import SVC, SVR

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

numerical_features = [
    col for col in X.columns
    if col not in categorical_features
]

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
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
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

# 9. Train SVC classification models
for target in classification_targets:

    print("\n" + "=" * 50)
    print("SVM CLASSIFICATION:", target)
    print("=" * 50)

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("model", SVC(
            kernel="rbf",
            C=1.0,
            class_weight="balanced"
        ))
    ])

    # Train model
    model.fit(X_train, y_train[target])

    # Predict
    predictions = model.predict(X_test)

    # Evaluate
    print("\nAccuracy:",
          accuracy_score(y_test[target], predictions))

    print("Macro F1 Score:",
          f1_score(
              y_test[target],
              predictions,
              average="macro"
          ))

    print("Balanced Accuracy:",
          balanced_accuracy_score(
              y_test[target],
              predictions
          ))

    print("\nClassification Report:")
    print(classification_report(
        y_test[target],
        predictions,
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(
        y_test[target],
        predictions
    ))

    # Save model
    filename = f"models/svm_{target.lower().replace(' ', '_')}.pkl"

    joblib.dump(model, filename)

    print("\nModel saved:", filename)


# 10. Train SVR regression models
for target in regression_targets:

    print("\n" + "=" * 50)
    print("SVM REGRESSION:", target)
    print("=" * 50)

    model = Pipeline([
        ("preprocessing", preprocessor),
        ("model", SVR(
            kernel="rbf",
            C=1.0,
            epsilon=0.1
        ))
    ])

    # Train model
    model.fit(X_train, y_train[target])

    # Predict
    predictions = model.predict(X_test)

    # Evaluate
    print("\nMean Absolute Error:",
          mean_absolute_error(y_test[target], predictions))

    print("Root Mean Squared Error:",
          root_mean_squared_error(y_test[target], predictions))

    print("R2 Score:",
          r2_score(y_test[target], predictions))

    # Save model
    filename = f"models/svm_{target.lower().replace(' ', '_')}.pkl"

    joblib.dump(model, filename)

    print("\nModel saved:", filename)


print("\n" + "=" * 50)
print("ALL SVM MODELS TRAINED SUCCESSFULLY!")
print("Models saved inside the models folder.")
print("=" * 50)
