from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer, UserLoginSerializer, TokenSerializer


class UserRegisterAPIView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )


# 로그인 상태라면 토큰이 헤더에 있을 것인데 굳이 바디에 넣으라는 게 이상하다.
class UserLogoutAPIView(GenericAPIView):
    # lookup_field = "auth_token"     # lookup_field는 model의 필드라고 하는데, seiralizer의 필드값을 넣어주는 것이 왜 가능한 것인지 모르겠다.
    queryset = Token.objects.all()
    serializer_class = TokenSerializer  # 없어도 되지 않을까 싶다. Tokenauthetication에서 자동으로 해주지 않을까...?

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Token.objects.get(key=request.data['auth_token']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
