from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AnalyzeRequestSerializer, SummariesSerializer, ArticlesSerializer
from .models import Summaries, Articles
from datetime import datetime
import sys
sys.path.append('../sentiment_analysis')
from analysis_module import analysis_wrapper
import numpy as np



def main(request):
    return HttpResponse('Hello World')


class SummariesView(generics.ListAPIView):
    queryset = Summaries.objects.all()
    serializer_class = SummariesSerializer
    

class ArticlesView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer


def index(request, *arg, **kwargs):
    return render(request, 'frontend/index.html')


class AnalyzeRequestView(APIView):
    serializer_class = AnalyzeRequestSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ticker = serializer.data.get('ticker')
            current_date = datetime.today().strftime('%Y-%m-%d')
            # run analysis
            article_records = analysis_wrapper(ticker)
            for article_record in article_records:
                # search if article already exists in database
                # from previous analysis runs
                query = Articles.objects.filter(link=article_record.link)
                if not query.exists():                   
                    # only create new record if it doesn't
                    new_record = Articles(ticker=ticker,
                                        title=article_record.title,
                                        date=article_record.date,
                                        link=article_record.link,
                                        pos_score=article_record.pos_score,
                                        neg_score=article_record.neg_score,
                                        overall_rating=article_record.overall_rating)
                    new_record.save()
                
            
            # new_summary = Summaries(ticker=ticker, date=current_date, overall_rating=overall_rating)
            # new_summary.save()
                
            return Response(status=status.HTTP_201_CREATED)
