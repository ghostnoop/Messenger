from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from main.models import User, Chat, Message


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                _('A user with this email and password was not found.')
            )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['user']
        chat = Chat.objects.create(title=validated_data.get('title'))
        chat.users.add(user)
        chat.save()
        return chat


class ChatFullSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['id', 'title', 'users']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'created_at', 'read', 'text', 'media']
        read_only_fields = ['id', 'user', 'created_at', 'read']
        optional_fields = ['text', 'media']

    def create(self, validated_data):
        chat_id = self.context.get('chat_id')
        if chat_id is None:
            raise serializers.ValidationError(
                _('chat_id is null')
            )
        text = validated_data.get('text')
        media = validated_data.get('media')
        if text is None and media is None:
            raise serializers.ValidationError(
                _('text and media are null')
            )

        user = self.context.get('user')
        message = Message.objects.create(user=user, chat_id=chat_id, **validated_data)
        return message
