
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    balanced_accuracy_score,
    hamming_loss,
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)

# 1. Load dataset
df = pd.read_excel("dataset/Risk_data.xlsx")

df = df.drop(columns=["Project ID"])

# 2. Separate features and targets
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

y_class = df[classification_targets]
y_reg = df[regression_targets]

# 3. Recreate the same train-test split
(
    X_train,
    X_test,
    y_class_train,
    y_class_test,
    y_reg_train,
    y_reg_test
) = train_test_split(
    X,
    y_class,
    y_reg,
    test_size=0.20,
    random_state=42,
    stratify=y_class["Risk Type"]
)

results = []

# 4. Evaluate Decision Tree classification
print("\nDECISION TREE CLASSIFICATION")

dt_classifier = joblib.load(
    "models/decision_tree_classifier.pkl"
)

dt_class_predictions = dt_classifier.predict(X_test)

dt_class_df = pd.DataFrame(
    dt_class_predictions,
    columns=classification_targets
)

dt_hamming = (
    y_class_test.to_numpy() != dt_class_predictions
).mean()

dt_exact_match = (
    y_class_test.to_numpy() == dt_class_predictions
).all(axis=1).mean()

print("Hamming Loss:", dt_hamming)
print("Exact Match Ratio:", dt_exact_match)

for i, target in enumerate(classification_targets):

    actual = y_class_test[target]
    predicted = dt_class_predictions[:, i]

    results.append({
        "Algorithm": "Decision Tree",
        "Target": target,
        "Accuracy": accuracy_score(actual, predicted),
        "Macro F1": f1_score(
            actual, predicted, average="macro"
        ),
        "Balanced Accuracy": balanced_accuracy_score(
            actual, predicted
        ),
        "Hamming Loss": dt_hamming,
        "Exact Match Ratio": dt_exact_match,
        "MAE": None,
        "RMSE": None,
        "R2 Score": None
    })


# 5. Evaluate other classification models
algorithms = [
    "random_forest",
    "logistic_regression",
    "svm",
    "xgboost"
]

for target in classification_targets:

    for algorithm in algorithms:

        path = (
            f"models/{algorithm}_"
            f"{target.lower().replace(' ', '_')}.pkl"
        )

        saved_model = joblib.load(path)

        if algorithm == "xgboost":

            model = saved_model["pipeline"]
            encoder = saved_model["label_encoder"]

            encoded_predictions = model.predict(X_test)

            predictions = encoder.inverse_transform(
                encoded_predictions.astype(int)
            )

        else:
            predictions = saved_model.predict(X_test)

        actual = y_class_test[target]

        results.append({
            "Algorithm": algorithm.replace("_", " ").title(),
            "Target": target,
            "Accuracy": accuracy_score(actual, predictions),
            "Macro F1": f1_score(
                actual, predictions, average="macro"
            ),
            "Balanced Accuracy": balanced_accuracy_score(
                actual, predictions
            ),
            "Hamming Loss": None,
            "Exact Match Ratio": None,
            "MAE": None,
            "RMSE": None,
            "R2 Score": None
        })


# 6. Evaluate Decision Tree regression
print("\nDECISION TREE REGRESSION")

dt_regressor = joblib.load(
    "models/decision_tree_regressor.pkl"
)

dt_reg_predictions = dt_regressor.predict(X_test)

for i, target in enumerate(regression_targets):

    actual = y_reg_test[target]
    predicted = dt_reg_predictions[:, i]

    results.append({
        "Algorithm": "Decision Tree",
        "Target": target,
        "Accuracy": None,
        "Macro F1": None,
        "Balanced Accuracy": None,
        "Hamming Loss": None,
        "Exact Match Ratio": None,
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": root_mean_squared_error(actual, predicted),
        "R2 Score": r2_score(actual, predicted)
    })


# 7. Evaluate other regression models
regression_algorithms = [
    "random_forest",
    "svm",
    "xgboost"
]

for target in regression_targets:

    for algorithm in regression_algorithms:

        path = (
            f"models/{algorithm}_"
            f"{target.lower().replace(' ', '_')}.pkl"
        )

        model = joblib.load(path)

        predictions = model.predict(X_test)

        actual = y_reg_test[target]

        results.append({
            "Algorithm": algorithm.replace("_", " ").title(),
            "Target": target,
            "Accuracy": None,
            "Macro F1": None,
            "Balanced Accuracy": None,
            "Hamming Loss": None,
            "Exact Match Ratio": None,
            "MAE": mean_absolute_error(actual, predictions),
            "RMSE": root_mean_squared_error(actual, predictions),
            "R2 Score": r2_score(actual, predictions)
        })


# 8. Create final comparison table
comparison_df = pd.DataFrame(results)

print("\n" + "=" * 90)
print("FINAL CLASSIFICATION COMPARISON")
print("=" * 90)

print(
    comparison_df[
        comparison_df["Target"].isin(classification_targets)
    ].round(4).to_string(index=False)
)

print("\n" + "=" * 90)
print("FINAL REGRESSION COMPARISON")
print("=" * 90)

print(
    comparison_df[
        comparison_df["Target"].isin(regression_targets)
    ].round(4).to_string(index=False)
)

# 9. Save results
os.makedirs("results", exist_ok=True)

comparison_df.to_csv(
    "results/final_model_comparison.csv",
    index=False
)

print("\nFINAL MODEL COMPARISON COMPLETED!")
print("Saved: results/final_model_comparison.csv")
