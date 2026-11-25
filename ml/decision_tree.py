
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor

from sklearn.metrics import (
    hamming_loss,
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)

# 1. Load dataset
df = pd.read_excel("dataset/Risk_data.xlsx")

# 2. Remove Project ID
df = df.drop(columns=["Project ID"])

# 3. Separate input features and targets
X = df.drop(columns=[
    "Risk Type",
    "Risk Impact",
    "Risk Probability",
    "Risk Response Plan"
])

classification_targets = [
    "Risk Type",
    "Risk Response Plan"
]

regression_targets = [
    "Risk Impact",
    "Risk Probability"
]

y_classification = df[classification_targets]
y_regression = df[regression_targets]

# 4. Identify categorical features
categorical_features = ["Project Industry"]

# 5. Split dataset
(
    X_train,
    X_test,
    y_class_train,
    y_class_test,
    y_reg_train,
    y_reg_test
) = train_test_split(
    X,
    y_classification,
    y_regression,
    test_size=0.20,
    random_state=42,
    stratify=y_classification["Risk Type"]
)

# 6. Preprocessing using Ordinal Encoding
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# 7. Create models directory
os.makedirs("models", exist_ok=True)

# ==========================================
# 8. MULTI-OUTPUT DECISION TREE CLASSIFIER
# ==========================================

print("\n" + "=" * 55)
print("DECISION TREE MULTI-OUTPUT CLASSIFICATION")
print("=" * 55)

classification_model = Pipeline([
    ("preprocessing", preprocessor),
    ("model", MultiOutputClassifier(
        DecisionTreeClassifier(random_state=42)
    ))
])

# Train classifier
classification_model.fit(X_train, y_class_train)

# Predict
class_predictions = classification_model.predict(X_test)

class_predictions_df = pd.DataFrame(
    class_predictions,
    columns=classification_targets,
    index=y_class_test.index
)


# Calculate Hamming Loss manually
actual_values = y_class_test.to_numpy()

incorrect_predictions = (
    actual_values != class_predictions
)

h_loss = incorrect_predictions.mean()

# Calculate Exact Match Ratio
exact_match = (
    actual_values == class_predictions
).all(axis=1).mean()

print("\nHamming Loss:", h_loss)
print("Exact Match Ratio:", exact_match)
print("Exact Match Percentage:", exact_match * 100)


# Individual target accuracy for additional analysis
for i, target in enumerate(classification_targets):

    accuracy = (
        y_class_test[target].to_numpy()
        == class_predictions[:, i]
    ).mean()

    print(f"\n{target} Accuracy: {accuracy:.4f}")


# Save classification model
joblib.dump(
    classification_model,
    "models/decision_tree_classifier.pkl"
)

print("\nClassification model saved!")


# ==========================================
# 9. MULTI-OUTPUT DECISION TREE REGRESSOR
# ==========================================

print("\n" + "=" * 55)
print("DECISION TREE MULTI-OUTPUT REGRESSION")
print("=" * 55)

regression_model = Pipeline([
    ("preprocessing", preprocessor),
    ("model", MultiOutputRegressor(
        DecisionTreeRegressor(random_state=42)
    ))
])

# Train regressor
regression_model.fit(X_train, y_reg_train)

# Predict
reg_predictions = regression_model.predict(X_test)

reg_predictions_df = pd.DataFrame(
    reg_predictions,
    columns=regression_targets,
    index=y_reg_test.index
)

# Evaluate each regression target
for target in regression_targets:

    actual = y_reg_test[target]
    predicted = reg_predictions_df[target]

    print("\n" + "-" * 40)
    print("TARGET:", target)
    print("-" * 40)

    print(
        "Mean Absolute Error:",
        mean_absolute_error(actual, predicted)
    )

    print(
        "Root Mean Squared Error:",
        root_mean_squared_error(actual, predicted)
    )

    print(
        "R2 Score:",
        r2_score(actual, predicted)
    )


# Save regression model
joblib.dump(
    regression_model,
    "models/decision_tree_regressor.pkl"
)

print("\nRegression model saved!")

# ==========================================
# 10. COMPLETION
# ==========================================

print("\n" + "=" * 55)
print("DECISION TREE TRAINING COMPLETED!")
print("Both models saved inside the models folder.")
print("=" * 55)

