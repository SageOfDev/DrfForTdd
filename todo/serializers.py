from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from todo.models import Todo


class TodoUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class TodoSerializer(ModelSerializer):
    user = TodoUserSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = "__all__"

