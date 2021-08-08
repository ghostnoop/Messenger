# Create your views here.
from django.db.models import Q
from rest_framework import status, viewsets, authentication
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Chat, Message
from main.permissions.chat_permission import ChatForOnlySubscribers
from main.serializers import (RegistrationSerializer, LoginSerializer, ChatSerializer,
                              ChatFullSerializer, MessageSerializer)
from main.services.chat_service import chat_queryset
from main.services.user_service import token_from_user


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data.get('id')
        token = token_from_user(user_id)

        return Response(dict(user_pk=user_id, token=token.key), status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.data.get('id')
        token = token_from_user(user_id)

        return Response(dict(user_pk=user_id, token=token.key), status=status.HTTP_200_OK)


class ChatsViewSet(viewsets.ModelViewSet):
    """Чаты"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [ChatForOnlySubscribers, IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ChatFullSerializer
        return ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(users__id=user.pk)

    def get_serializer_context(self):
        context = super(ChatsViewSet, self).get_serializer_context()
        context.update(
            {'user': self.request.user}
        )
        return context


class ChatMessageAPIView(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    pagination_class = LimitOffsetPagination
    permission_classes = [ChatForOnlySubscribers, IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        qs = chat_queryset(**self.get_serializer_context())
        return qs

    def get_serializer_context(self):
        context = super(ChatMessageAPIView, self).get_serializer_context()
        context.update({
            'user': self.request.user,
            'chat_id': self.kwargs.get('pk', None)

        })
        return context

    def retrieve(self, request, pk=None, *args, **kwargs):
        return super(ChatMessageAPIView, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(ChatMessageAPIView, self).create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([ChatForOnlySubscribers, IsAuthenticated])
def message_read(request, message_id: int):
    message: Message = get_object_or_404(Message, Q(user=request.user, id=message_id))
    if not message.read:
        message.read = True
        message.save()
    return Response(status=200)
