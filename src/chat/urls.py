from django.urls import path

from django.urls import path

from chat import views

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("ws/", views.websocket_view),
]
