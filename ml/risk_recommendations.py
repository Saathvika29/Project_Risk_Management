
# Intelligent Risk Recommendations
# Project: An Intelligent Machine Learning-Based
# Decision Support System for Project Risk Prediction and Management

from risk_severity import analyze_risk


# Recommendation knowledge base
RECOMMENDATIONS = {

    "Technical": {
        "Low": [
            "Perform routine technical checks.",
            "Monitor system performance regularly."
        ],
        "Medium": [
            "Conduct regular software testing.",
            "Maintain technical documentation.",
            "Monitor system performance."
        ],
        "High": [
            "Conduct detailed technical testing.",
            "Maintain backup systems.",
            "Prepare a technical recovery plan."
        ],
        "Critical": [
            "Immediately investigate the technical issue.",
            "Activate backup and recovery systems.",
            "Conduct intensive system testing.",
            "Assign a dedicated technical team.",
            "Monitor system performance continuously."
        ]
    },

    "Financial": {
        "Low": [
            "Monitor project expenses.",
            "Review the financial budget periodically."
        ],
        "Medium": [
            "Review budget allocation.",
            "Track expenses regularly.",
            "Maintain a financial contingency reserve."
        ],
        "High": [
            "Conduct a detailed budget review.",
            "Control unnecessary expenditure.",
            "Prepare a financial contingency plan."
        ],
        "Critical": [
            "Immediately review the project budget.",
            "Identify major sources of financial loss.",
            "Reallocate financial resources.",
            "Activate the financial contingency plan.",
            "Monitor expenses closely."
        ]
    },

    "Operational": {
        "Low": [
            "Monitor daily project operations.",
            "Review operational procedures."
        ],
        "Medium": [
            "Improve operational planning.",
            "Monitor resource utilization.",
            "Review team responsibilities."
        ],
        "High": [
            "Improve operational workflows.",
            "Allocate resources efficiently.",
            "Prepare an alternative operational plan."
        ],
        "Critical": [
            "Immediately investigate operational failures.",
            "Reorganize critical project activities.",
            "Allocate additional resources.",
            "Implement alternative operational procedures.",
            "Monitor operational performance closely."
        ]
    },

    "Compliance": {
        "Low": [
            "Review applicable regulations.",
            "Maintain compliance documentation."
        ],
        "Medium": [
            "Conduct periodic compliance checks.",
            "Update regulatory documentation.",
            "Monitor changes in applicable regulations."
        ],
        "High": [
            "Conduct a compliance audit.",
            "Resolve identified regulatory gaps.",
            "Consult compliance professionals."
        ],
        "Critical": [
            "Immediately investigate compliance violations.",
            "Conduct a detailed compliance audit.",
            "Take corrective actions.",
            "Consult legal or compliance professionals.",
            "Ensure all regulatory requirements are fulfilled."
        ]
    }
}


def generate_recommendations(
    risk_name,
    risk_type,
    impact,
    probability
):
    """
    Generate intelligent risk recommendations
    based on risk type and severity.
    """

    # Calculate risk severity
    analysis = analyze_risk(
        impact,
        probability
    )

    severity = analysis["Severity"]

    # Retrieve suitable recommendations
    if risk_type not in RECOMMENDATIONS:
        raise ValueError(
            f"Unsupported risk type: {risk_type}"
        )

    recommendations = list(RECOMMENDATIONS[risk_type][severity])

    # Additional recommendation for high probability
    if probability >= 80:
        recommendations.append(
            "Increase risk monitoring frequency due to high probability."
        )

    return {
        "Risk Name": risk_name,
        "Risk Type": risk_type,
        "Impact": impact,
        "Probability": probability,
        "Risk Score": analysis["Risk Score"],
        "Severity": severity,
        "Recommendations": recommendations
    }


# Test the functionality
if __name__ == "__main__":

    project_risks = [

        {
            "Risk Name": "Technical Failure",
            "Risk Type": "Technical",
            "Impact": 9,
            "Probability": 90
        },

        {
            "Risk Name": "Budget Overrun",
            "Risk Type": "Financial",
            "Impact": 7,
            "Probability": 80
        },

        {
            "Risk Name": "Resource Shortage",
            "Risk Type": "Operational",
            "Impact": 4,
            "Probability": 60
        },

        {
            "Risk Name": "Regulatory Violation",
            "Risk Type": "Compliance",
            "Impact": 8,
            "Probability": 85
        }
    ]

    print("\nINTELLIGENT RISK RECOMMENDATIONS")
    print("=" * 75)

    for risk in project_risks:

        result = generate_recommendations(
            risk["Risk Name"],
            risk["Risk Type"],
            risk["Impact"],
            risk["Probability"]
        )

        print("\nRisk Name:", result["Risk Name"])
        print("Risk Type:", result["Risk Type"])
        print("Impact:", result["Impact"])
        print("Probability:", result["Probability"], "%")
        print("Risk Score:", result["Risk Score"])
        print("Severity:", result["Severity"])

        print("\nRecommended Actions:")

        for index, recommendation in enumerate(
            result["Recommendations"],
            start=1
        ):
            print(f"{index}. {recommendation}")

        print("-" * 75)
