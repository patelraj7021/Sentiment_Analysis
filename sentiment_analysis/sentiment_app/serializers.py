from rest_framework import serializers
from .models import Summaries, Articles


class SummariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summaries
        fields = ['id', 'ticker', 'date', 'overall_rating']
        
        
class AnalyzeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summaries
        fields = ['ticker']