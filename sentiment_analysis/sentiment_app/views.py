from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AnalyzeRequestSerializer, SummariesSerializer
from .models import Summaries
from datetime import datetime



def main(request):
    return HttpResponse('Hello World')


class SummariesView(generics.ListAPIView):
    queryset = Summaries.objects.all()
    serializer_class = SummariesSerializer


def index(request, *arg, **kwargs):
    return render(request, 'frontend/index.html')


class AnalyzeRequestView(APIView):
    serializer_class = AnalyzeRequestSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ticker = serializer.data.get('ticker')
            current_date = datetime.today().strftime('%Y-%m-%d')
            # queryset = Summaries.objects.filter(ticker=ticker, date=current_date)
            # if queryset.exists():
            #     debug_output = 'data exists'
            # else:
            #     new_summary = Summaries(ticker=ticker, date=current_date, overall_rating=50)
            #     new_summary.save()
            new_summary = Summaries(ticker=ticker, date=current_date, overall_rating=50)
            new_summary.save()
                
            return Response(SummariesSerializer(new_summary).data)
