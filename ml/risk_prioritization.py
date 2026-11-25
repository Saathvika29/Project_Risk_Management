
# Risk Prioritization
# Project: Intelligent ML-Based Decision Support System

import pandas as pd

from risk_severity import analyze_risk


def prioritize_risks(risks):
    """
    Calculate risk scores and rank risks
    from highest priority to lowest priority.
    """

    results = []

    for risk in risks:

        analysis = analyze_risk(
            risk["Impact"],
            risk["Probability"]
        )

        results.append({
            "Risk ID": risk["Risk ID"],
            "Risk Name": risk["Risk Name"],
            "Impact": analysis["Impact"],
            "Probability": analysis["Probability"],
            "Risk Score": analysis["Risk Score"],
            "Severity": analysis["Severity"]
        })

    # Sort risks by score in descending order
    results.sort(
        key=lambda x: x["Risk Score"],
        reverse=True
    )

    # Assign priority ranks
    for index, risk in enumerate(results, start=1):
        risk["Priority Rank"] = index

    return pd.DataFrame(results)


# Test the functionality
if __name__ == "__main__":

    project_risks = [

        {
            "Risk ID": 1,
            "Risk Name": "Technical Failure",
            "Impact": 9,
            "Probability": 90
        },

        {
            "Risk ID": 2,
            "Risk Name": "Budget Overrun",
            "Impact": 7,
            "Probability": 80
        },

        {
            "Risk ID": 3,
            "Risk Name": "Resource Shortage",
            "Impact": 4,
            "Probability": 60
        },

        {
            "Risk ID": 4,
            "Risk Name": "Schedule Delay",
            "Impact": 2,
            "Probability": 30
        },

        {
            "Risk ID": 5,
            "Risk Name": "Security Issues",
            "Impact": 8,
            "Probability": 85
        }
    ]

    priority_results = prioritize_risks(project_risks)

    print("\nRISK PRIORITIZATION")
    print("=" * 90)

    print(priority_results.to_string(index=False))

    print("\nHighest Priority Risk:")
    print(priority_results.iloc[0]["Risk Name"])
