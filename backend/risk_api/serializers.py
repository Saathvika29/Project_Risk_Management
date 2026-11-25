
from rest_framework import serializers


class RiskInputSerializer(serializers.Serializer):

    project_industry = serializers.CharField(max_length=100)

    project_duration = serializers.IntegerField()
    percentage_of_completion = serializers.IntegerField()
    initial_budget = serializers.IntegerField()
    cost_variance = serializers.IntegerField()
    scope_creep = serializers.IntegerField()
    technical_complexity = serializers.IntegerField()
    operational_efficiency = serializers.IntegerField()
    budget_changes = serializers.IntegerField()
    regulations_impact = serializers.IntegerField()
    deviations_from_strategic_goals = serializers.IntegerField()
    market_fluctuations = serializers.IntegerField()
    reputational_impact = serializers.IntegerField()
    environmental_impact = serializers.IntegerField()
    legal_challenges = serializers.IntegerField()
    security_threats = serializers.IntegerField()
    supply_chain_disruptions = serializers.IntegerField()
    hr_issues = serializers.IntegerField()
    schedule_changes = serializers.IntegerField()
    schedule_variance = serializers.IntegerField()
    stakeholder_issues = serializers.IntegerField()
    stakeholder_engagement_level = serializers.IntegerField()
    stakeholder_influence_level = serializers.IntegerField()
    external_dependencies = serializers.IntegerField()
    economic_conditions = serializers.IntegerField()
    quality_issues = serializers.IntegerField()
