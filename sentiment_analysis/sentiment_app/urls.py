from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('past_entries', views.AnalysisView.as_view())
]