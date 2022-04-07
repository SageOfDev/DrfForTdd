from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # 아래 confrim_pasword는 user 모델에는 없으나 validation 용으로만 사용되는 듯하다.
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password", "date_joined"]

    def validate(self, data):
        if data.get('password') != data.get('confirm_apssword'):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        del data['confirm_password']
        # `make_password`는 해싱된 암호를 만들어준다. salt나 해시 알고리즘을 선택할 수 있다.
        data['password'] = make_password(data['password'])
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': '비활성화 된 계정입니다.',
        'unathorized_account': '인가받지 못한 계정입니다.',
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        self.user = authenticate(username=data.get("username"), password=data.get("password"))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return data
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

