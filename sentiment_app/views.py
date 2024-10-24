from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AnalyzeRequestSerializer, SummariesSerializer, \
    ArticlesSerializer, TopArticlesSerializer, SummaryCircleSerializer
from .models import Summaries, Articles
from datetime import datetime, timedelta
# import sys
# sys.path.append('../sentiment_analysis')
# from analysis_module import crawling_wrapper, analyze_article
from query_ticker import query_ticker
import numpy as np
import os



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
            # current_date = datetime.today().strftime('%Y-%m-%d')
            current_date = datetime.today()
            
            try:
                query_ticker(ticker)
            except:
                return Response(status=status.HTTP_417_EXPECTATION_FAILED)
            
            # average over the ratings of articles from past 3 days for Summaries table   
            past_3days_articles = Articles.objects.filter(date__range=[current_date-timedelta(days=4),
                                                                      current_date],
                                                         ticker=ticker)
            if past_3days_articles.count() == 0:
                # 50 is the default rating on the UI, so it won't update anything
                avg_rating = 50
            else:
                avg_rating = int(past_3days_articles.aggregate(Avg("overall_rating"))['overall_rating__avg'])
            try:
                # update record for the day if it exists
                query = Summaries.objects.get(ticker=ticker, date=current_date.strftime('%Y-%m-%d'))
                query.overall_rating = avg_rating
                query.save(update_fields=['overall_rating'])
            except:
                # create a new one if it doesn't
                new_summary = Summaries(ticker=ticker, 
                                        date=current_date.strftime('%Y-%m-%d'), 
                                        overall_rating=avg_rating)
                new_summary.save()
                
            return Response(status=status.HTTP_201_CREATED)
        
        
class TopArticlesView(APIView):
    # return top 4 highest/lowest rated articles for a stock
    serializer_class = TopArticlesSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ticker = serializer.data.get('ticker')
            sort_order = serializer.data.get('sort_order')
            current_date = datetime.today()
            queryset = Articles.objects.filter(ticker=ticker, 
                                               date__range=[current_date-timedelta(days=4), 
                                                            current_date])                                                        
            queryset_ordered = queryset.order_by(f'{sort_order}')[:4]
            
            return Response(ArticlesSerializer(queryset_ordered, many=True).data, 
                            status=status.HTTP_200_OK)


class SummaryCircleView(APIView):
    # return average ratings over date_delta num days
    serializer_class = SummaryCircleSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ticker = serializer.data.get('ticker')
            date_delta = serializer.data.get('date_delta')
            current_date = datetime.today()
            queryset = Articles.objects.filter(ticker=ticker, 
                                               date__range=[current_date-timedelta(days=date_delta), 
                                                            current_date])
            if queryset.count() == 0:
                # 50 is the default rating on the UI, so it won't update anything
                avg_rating = 50
            else:
                avg_rating = int(queryset.aggregate(Avg("overall_rating"))['overall_rating__avg'])
            result = Summaries(ticker=ticker, 
                               date=current_date.strftime('%Y-%m-%d'), 
                               overall_rating=avg_rating)
            
            return Response(SummariesSerializer(result).data, 
                            status=status.HTTP_200_OK)
            

class HistoricalView(APIView):
    # return 3 day averaged ratings for last 30 days from Summaries table
    serializer_class = AnalyzeRequestSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ticker = serializer.data.get('ticker')
            current_date = datetime.today()
            date_delta = 31
            queryset = Summaries.objects.filter(ticker=ticker, 
                                                date__range=[current_date-timedelta(days=date_delta), 
                                                            current_date])
            return Response(SummariesSerializer(queryset, many=True).data, 
                            status=status.HTTP_200_OK)
            