
# Risk Interdependency Analysis
# Project: Intelligent ML-Based Decision Support System

import networkx as nx
import matplotlib.pyplot as plt


def analyze_interdependencies(risks, relationships):
    """
    Create a directed graph of project risks
    and analyse their interdependencies.

    risks: List of risk dictionaries
    relationships: List of directed risk pairs
    """

    graph = nx.DiGraph()

    # Add risk nodes
    for risk in risks:
        graph.add_node(
            risk["Risk Name"],
            severity=risk["Severity"],
            score=risk["Risk Score"]
        )

    # Add relationships between risks
    for source, target in relationships:

        if source not in graph or target not in graph:
            raise ValueError(
                f"Unknown risk in relationship: {source} -> {target}"
            )

        graph.add_edge(source, target)

    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(graph)
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())

    print("\nRISK INTERDEPENDENCY ANALYSIS")
    print("=" * 75)

    print("\nRisk Relationship Details:")

    for source, target in graph.edges():
        print(f"{source} --> {target}")

    print("\nRisk Connection Analysis:")
    print("-" * 75)

    for risk in graph.nodes():

        print(f"\nRisk: {risk}")
        print(f"Degree Centrality: {degree_centrality[risk]:.3f}")
        print(f"Incoming Connections: {in_degree[risk]}")
        print(f"Outgoing Connections: {out_degree[risk]}")

    # Identify the most connected risk
    most_connected = max(
        degree_centrality,
        key=degree_centrality.get
    )

    print("\nMost Connected Risk:")
    print(most_connected)

    return graph


def visualize_network(graph):

    plt.figure(figsize=(12, 8))

    positions = nx.spring_layout(
        graph,
        seed=42
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=2800,
        node_color="skyblue"
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=9,
        font_weight="bold"
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowsize=20,
        edge_color="gray",
        connectionstyle="arc3,rad=0.08"
    )

    plt.title(
        "Project Risk Interdependency Network",
        fontsize=15
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        "results/risk_interdependency_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# Test the functionality
if __name__ == "__main__":

    # Example project risks
    project_risks = [

        {
            "Risk Name": "Technical Failure",
            "Severity": "Critical",
            "Risk Score": 8.1
        },

        {
            "Risk Name": "Schedule Delay",
            "Severity": "Low",
            "Risk Score": 0.6
        },

        {
            "Risk Name": "Budget Overrun",
            "Severity": "High",
            "Risk Score": 5.6
        },

        {
            "Risk Name": "Resource Shortage",
            "Severity": "Medium",
            "Risk Score": 2.4
        },

        {
            "Risk Name": "Security Issues",
            "Severity": "Critical",
            "Risk Score": 6.8
        }
    ]

    # Illustrative directed relationships
    relationships = [

        ("Technical Failure", "Schedule Delay"),

        ("Schedule Delay", "Budget Overrun"),

        ("Resource Shortage", "Schedule Delay"),

        ("Security Issues", "Technical Failure"),

        ("Security Issues", "Budget Overrun")

    ]

    # Perform analysis
    risk_graph = analyze_interdependencies(
        project_risks,
        relationships
    )

    # Generate network visualization
    visualize_network(risk_graph)
