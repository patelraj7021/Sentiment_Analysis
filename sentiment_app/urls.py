from django.urls import path
from . import views

urlpatterns = [
    # path('', views.main),
    path('past-summaries', views.SummariesView.as_view()),
    path('past-articles', views.ArticlesView.as_view()),
    path('analyze-request', views.AnalyzeRequestView.as_view()),
    path('top-articles', views.TopArticlesView.as_view()),
    path('summary-circle', views.SummaryCircleView.as_view()),
    path('historical', views.HistoricalView.as_view()),
    path('', views.index)
]