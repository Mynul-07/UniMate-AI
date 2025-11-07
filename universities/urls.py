from django.urls import path
from .views import (
    UniversityListView, UniversityDetailView, search_universities,
    list_programs, list_fees, list_scholarships, list_hidden_charges,
    MetricListView
)

urlpatterns = [
    path("", UniversityListView.as_view()),
    path("<int:pk>/", UniversityDetailView.as_view()),
    path("search/", search_universities),
    path("<int:pk>/programs/", list_programs),
    path("<int:pk>/fees/", list_fees),
    path("<int:pk>/scholarships/", list_scholarships),
    path("<int:pk>/hidden-charges/", list_hidden_charges),
    path("metrics/", MetricListView.as_view()),
]
