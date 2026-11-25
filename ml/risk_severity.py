
# Risk Severity Analysis
# Project: Intelligent ML-Based Decision Support System

import pandas as pd


def calculate_risk_score(impact, probability):
    """
    Calculate risk score using impact and probability.
    Impact: 1 to 10
    Probability: 0 to 100
    """

    if not 1 <= impact <= 10:
        raise ValueError("Impact must be between 1 and 10")

    if not 0 <= probability <= 100:
        raise ValueError("Probability must be between 0 and 100")

    return impact * (probability / 100)


def classify_severity(risk_score):
    """
    Classify risk based on calculated risk score.
    """

    if risk_score <= 2:
        return "Low"

    elif risk_score <= 4:
        return "Medium"

    elif risk_score <= 6:
        return "High"

    else:
        return "Critical"


def analyze_risk(impact, probability):
    """
    Perform complete risk severity analysis.
    """

    risk_score = calculate_risk_score(
        impact, probability
    )

    severity = classify_severity(risk_score)

    return {
        "Impact": impact,
        "Probability": probability,
        "Risk Score": round(risk_score, 2),
        "Severity": severity
    }


# Test the functionality
if __name__ == "__main__":

    test_risks = [
        (2, 30),
        (4, 60),
        (7, 80),
        (9, 90),
        (5, 40)
    ]

    results = []

    for impact, probability in test_risks:

        result = analyze_risk(
            impact, probability
        )

        results.append(result)

    df = pd.DataFrame(results)

    print("\nRISK SEVERITY ANALYSIS")
    print("=" * 60)

    print(df.to_string(index=False))
