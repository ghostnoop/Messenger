from django.db.models import Q, QuerySet
from itertools import chain

from django.utils.datastructures import MultiValueDict
from rest_framework.request import Request

from main.models import Chat, Message
from main.models.user import Role, User


def chat_queryset(chat_id, user, *args, **kwargs) -> QuerySet[Message]:
    if user.role == Role.admin:
        query = Q(chat_id=chat_id)
    else:
        query = Q(chat_id=chat_id, chat__users__id=user.id)

    qs = Message.objects.filter(query).order_by('-id')
    messages_read(qs, user)
    return qs


def messages_read(messages: QuerySet[Message], current_user: User):
    to_update = []
    for message in messages:
        if message.user_id != current_user.id and not message.read:
            to_update.append(message)
    if to_update:
        Message.objects.bulk_update(to_update, fields=['read'])
