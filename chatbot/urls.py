from django.urls import path
from .views import ChatView, HistoryView, SessionDetailView, ContextView

urlpatterns = [
    path("", ChatView.as_view()),
    path("history/", HistoryView.as_view()),
    path("<uuid:session_id>/", SessionDetailView.as_view()),
    path("context/", ContextView.as_view()),
]
