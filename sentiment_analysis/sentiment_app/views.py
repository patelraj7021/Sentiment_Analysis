from django.shortcuts import render
from django.http import HttpResponse
from .serializers import AnalysisSerializer
from .models import Analysis
from rest_framework import generics


def main(request):
    return HttpResponse('Hello World')

class AnalysisView(generics.CreateAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

def index(request, *arg, **kwargs):
    return render(request, 'frontend/index.html')