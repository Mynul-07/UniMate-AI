from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/universities/", include("universities.urls")),
    path("api/chat/", include("chatbot.urls")),
    path("api/recommendations/", include("recommendations.urls")),
    path("api/token/", include("users.jwt_urls")),  # obtain/refresh tokens
]
