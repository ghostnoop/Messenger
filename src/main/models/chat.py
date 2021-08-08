from django.db import models

from main.models.base import BaseModel
from main.services.models_service import message_upload_path_create


class Chat(BaseModel):
    users = models.ManyToManyField("User", related_name='chat_users')
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat'


class MessageBase(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Message(MessageBase):
    text = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to=message_upload_path_create, null=True, blank=True)

    class Meta:
        db_table = 'message'
