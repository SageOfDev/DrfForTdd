from rest_framework.generics import CreateAPIView

from users.serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegisterSerializer