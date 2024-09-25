from django.urls import path
from . import views

urlpatterns = [
    # path('', views.main),
    path('past-summaries', views.SummariesView.as_view()),
    path('analyze-request', views.AnalyzeRequestView.as_view()),
    path('', views.index)
]