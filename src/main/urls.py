from django.urls import path
from rest_framework.routers import SimpleRouter

from main import views

router = SimpleRouter()
router.register("chats", views.ChatsViewSet, "chats")
router.register("messages", views.ChatMessageAPIView, "messages")

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    *router.urls,
    # path('messages/<int:chat_id>/', views.ChatMessageAPIView.as_view())

]
