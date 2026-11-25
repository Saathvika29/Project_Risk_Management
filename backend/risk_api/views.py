from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import RiskInputSerializer

from .ml_service import (
    predict_project_risk,
    analyze_risk,
    prioritize_project_risks,
    analyze_project_interdependencies,
    get_project_risk_recommendations
)


# HOME API
@api_view(["GET"])
def home(request):
    return Response({
        "message": "Project Risk Management API is running!",
        "status": "success"
    })


# 1. ML RISK PREDICTION API
@api_view(["POST"])
def predict_risk(request):

    serializer = RiskInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        predictions = predict_project_risk(
            serializer.validated_data
        )

        return Response({
            "message": "Risk prediction successful!",
            "predictions": predictions
        })

    except Exception as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 2. RISK SEVERITY API
@api_view(["POST"])
def risk_severity(request):

    try:
        impact = float(request.data["impact"])
        probability = float(request.data["probability"])

        result = analyze_risk(impact, probability)

        return Response({
            "message": "Risk severity analysis successful!",
            "result": result
        })

    except (KeyError, TypeError, ValueError) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )


# 3. RISK PRIORITIZATION API
@api_view(["POST"])
def risk_prioritization(request):

    risks = request.data.get("risks")

    if not isinstance(risks, list) or not risks:
        return Response(
            {"error": "Please provide a non-empty list of risks."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = prioritize_project_risks(risks)

        return Response({
            "message": "Risk prioritization successful!",
            "prioritized_risks": result
        })

    except (KeyError, TypeError, ValueError) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )


# 4. RISK INTERDEPENDENCY API
@api_view(["POST"])
def risk_interdependencies(request):

    risks = request.data.get("risks")
    relationships = request.data.get("relationships")

    if not isinstance(risks, list) or not risks:
        return Response(
            {"error": "Please provide a non-empty list of risks."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(relationships, list):
        return Response(
            {"error": "Please provide a list of risk relationships."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = analyze_project_interdependencies(
            risks,
            relationships
        )

        return Response({
            "message": "Risk interdependency analysis successful!",
            "result": result
        })

    except (KeyError, TypeError, ValueError) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )


# 5. INTELLIGENT RISK RECOMMENDATIONS API
@api_view(["POST"])
def risk_recommendations(request):

    try:
        result = get_project_risk_recommendations(
            risk_name=request.data["risk_name"],
            risk_type=request.data["risk_type"],
            impact=float(request.data["impact"]),
            probability=float(request.data["probability"])
        )

        return Response({
            "message": "Risk recommendations generated successfully!",
            "result": result
        })

    except (KeyError, TypeError, ValueError) as error:
        return Response(
            {"error": str(error)},
            status=status.HTTP_400_BAD_REQUEST
        )

