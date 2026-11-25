import sys
import joblib
import pandas as pd
import networkx as nx

from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

ML_DIR = BASE_DIR / "ml"
sys.path.insert(0, str(ML_DIR))

from risk_severity import analyze_risk
from risk_prioritization import prioritize_risks
from risk_interdependency import analyze_interdependencies
from risk_recommendations import generate_recommendations
MODEL_DIR = ML_DIR / "models"


# Original dataset feature names and their API names
FEATURE_MAPPING = {
    "project_industry": "Project Industry",
    "project_duration": "Project Duration",
    "percentage_of_completion": "Percentage of Completion",
    "initial_budget": "Initial Budget",
    "cost_variance": "Cost Variance",
    "scope_creep": "Scope Creep",
    "technical_complexity": "Technical Complexity",
    "operational_efficiency": "Operational Efficiency",
    "budget_changes": "Budget Changes",
    "regulations_impact": "Regulations Impact",
    "deviations_from_strategic_goals": "Deviations from Strategic Goals",
    "market_fluctuations": "Market Fluctuations",
    "reputational_impact": "Reputational Impact",
    "environmental_impact": "Environmental Impact",
    "legal_challenges": "Legal Challenges",
    "security_threats": "Security Threats",
    "supply_chain_disruptions": "Supply Chain Disruptions",
    "hr_issues": "HR Issues",
    "schedule_changes": "Schedule Changes",
    "schedule_variance": "Schedule Variance",
    "stakeholder_issues": "Stakeholder Issues",
    "stakeholder_engagement_level": "Stakeholder Engagement Level",
    "stakeholder_influence_level": "Stakeholder Influence Level",
    "external_dependencies": "External Dependencies",
    "economic_conditions": "Economic Conditions",
    "quality_issues": "Quality Issues"
}


# Load fitted preprocessing object
tree_preprocessor = joblib.load(
    MODEL_DIR / "tree_preprocessor.pkl"
)


# Load trained Random Forest models
risk_type_model = joblib.load(
    MODEL_DIR / "random_forest_risk_type.pkl"
)

risk_impact_model = joblib.load(
    MODEL_DIR / "random_forest_risk_impact.pkl"
)

risk_probability_model = joblib.load(
    MODEL_DIR / "random_forest_risk_probability.pkl"
)

response_plan_model = joblib.load(
    MODEL_DIR / "random_forest_risk_response_plan.pkl"
)


def predict_project_risk(input_data):
    """
    Generate four risk predictions using
    the trained Random Forest models.
    """

    # Convert API field names into dataset column names
    formatted_data = {
        original_name: input_data[api_name]
        for api_name, original_name in FEATURE_MAPPING.items()
    }

    # Create DataFrame in the original feature order
    input_df = pd.DataFrame(
        [formatted_data],
        columns=list(FEATURE_MAPPING.values())
    )

      # Generate predictions
    # The saved Random Forest pipelines already contain preprocessing

    risk_type = risk_type_model.predict(input_df)[0]
    risk_impact = risk_impact_model.predict(input_df)[0]
    risk_probability = risk_probability_model.predict(input_df)[0]
    response_plan = response_plan_model.predict(input_df)[0]
    severity_analysis = analyze_risk(
    float(risk_impact),
    float(risk_probability)
)
    
    return {
    "risk_type": str(risk_type),
    "risk_impact": round(float(risk_impact), 2),
    "risk_probability": round(float(risk_probability), 2),
    "risk_response_plan": str(response_plan),
    "risk_severity": severity_analysis
}
def prioritize_project_risks(risks):

    prioritized_results = prioritize_risks(risks)

    return prioritized_results.to_dict(orient="records")

def analyze_project_interdependencies(risks, relationships):

    graph = analyze_interdependencies(risks, relationships)

    degree_centrality = nx.degree_centrality(graph)
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())

    risk_analysis = []

    for risk in graph.nodes():

        risk_analysis.append({
            "risk_name": risk,
            "degree_centrality": round(degree_centrality[risk], 3),
            "incoming_connections": in_degree[risk],
            "outgoing_connections": out_degree[risk]
        })

    most_connected = max(
        degree_centrality,
        key=degree_centrality.get
    )

    return {
        "risk_relationships": [
            {"source": source, "target": target}
            for source, target in graph.edges()
        ],
        "risk_analysis": risk_analysis,
        "most_connected_risk": most_connected
    }

def get_project_risk_recommendations(
    risk_name,
    risk_type,
    impact,
    probability
):

    recommendations = generate_recommendations(
        risk_name,
        risk_type,
        impact,
        probability
    )

    return recommendations