from django.urls import path
from . import views

urlpatterns = [
    # path('', views.main),
    path('past-summaries', views.SummariesView.as_view()),
    path('past-articles', views.ArticlesView.as_view()),
    path('analyze-request', views.AnalyzeRequestView.as_view()),
    path('update-summary', views.UpdateSummaryCircle.as_view()),
    path('', views.index)
]