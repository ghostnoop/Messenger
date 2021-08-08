from rest_framework.permissions import BasePermission

from main.models import MessageBase
from main.models.user import Role


class ChatForOnlySubscribers(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin:
            return True
        return obj.users.filter(id=request.user.id).exists()


class MessagesOnlyFromChat(BasePermission):
    def has_object_permission(self, request, view, obj: MessageBase):
        if not request.user.is_authenticated:
            return False
        if request.user.role == Role.admin:
            return True
        return obj.chat.users.filter(id=request.user.id).exists()
