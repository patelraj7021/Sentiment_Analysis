from rest_framework import serializers
from .models import Summaries, Articles


class SummariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summaries
        fields = ['id', 'ticker', 'date', 'overall_rating']
        

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['id', 'ticker', 'title', 'date', 'link', 
                  'pos_score', 'neg_score', 'overall_rating']
        
        
class AnalyzeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summaries
        fields = ['ticker']
        

class TopArticlesSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=8)
    sort_order = serializers.CharField(max_length=16)
    