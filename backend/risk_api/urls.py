from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("predict/", views.predict_risk, name="predict-risk"),

    path("severity/", views.risk_severity, name="risk-severity"),

    path("prioritize/", views.risk_prioritization, name="risk-prioritization"),

    path("interdependencies/", views.risk_interdependencies, name="risk-interdependencies"),

    path("recommendations/", views.risk_recommendations, name="risk-recommendations"),
]
