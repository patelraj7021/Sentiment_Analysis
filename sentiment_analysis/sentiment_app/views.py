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
import sys
sys.path.append('../sentiment_analysis')
from analysis_module import crawling_wrapper, analyze_article
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
            # run crawling
            data_filepath = crawling_wrapper(ticker)
            # loop through scraped articles for Articles table
            for article_file in os.listdir(data_filepath):
                with open(os.path.join(data_filepath, article_file), 'r') as file:
                    data_input = file.read().split('\n')
                    # get link from article data file
                    article_link = data_input[1]
                    # search if article already exists in database
                    # from previous analysis runs
                    query = Articles.objects.filter(link=article_link, ticker=ticker)
                    if not query.exists():                   
                        # only run analysis if it doesn't
                        article_analysis = analyze_article(data_input, ticker)
                        if article_analysis is not None:
                            new_record = Articles(ticker=ticker, 
                                                title=article_analysis.title,
                                                date=article_analysis.date,
                                                link=article_analysis.link,
                                                pos_score=article_analysis.pos_score,
                                                neg_score=article_analysis.neg_score,
                                                overall_rating=article_analysis.overall_rating)
                            new_record.save()
            
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
            