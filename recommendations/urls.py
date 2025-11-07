from django.urls import path
from .views import UniversityRecommendationView, SubjectRecommendationView, HistoryView

urlpatterns = [
    path("university/", UniversityRecommendationView.as_view()),
    path("subject/", SubjectRecommendationView.as_view()),
    path("history/", HistoryView.as_view()),
]
