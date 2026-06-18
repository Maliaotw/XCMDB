from django.urls import path

from common import views as common_views

urlpatterns = [
    path("user/", common_views.UserAPIView.as_view()),
]
