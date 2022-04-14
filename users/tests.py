import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse('users:list')

    def test_invalid_password(self):
        """
        회원가입 - 패스워드 불일치
        """
        user_data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': 'password',
            'confirm_password': 'INVALID_PASSWORD'
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        회원가입 - 정상 가입
        """
        user_data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': '123123',
            'confirm_password': '123123'
        }
        response = self.client.post(self.url, user_data)
        print(json.loads(response.content))
        self.assertEqual(201, response.status_code)
        self.assertTrue('token' in json.loads(response.content))

    def test_unique_username_validation(self):
        """
        회원가입 - 중복가입(이름)
        """
        user_data_1 = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': '123123',
            'confirm_password': '123123'
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': '123123',
            'confirm_password': '123123'
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse('users:login')
    cnt = 0
    def setUp(self):
        """
        셋업 - 유저 생성
        """
        UserLoginAPIViewTestCase.cnt += 1
        print(UserLoginAPIViewTestCase.cnt, "hello")
        self.username = 'loginuser'
        self.email = 'loginuser@loginuser.com'
        self.password = 'loginuser123'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_passowrd(self):
        """
        로그인 - 패스워드 없이
        """
        response = self.client.post(self.url, {'username': self.username})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_passowrd(self):
        """
        로그인 - 틀린 패스워드 사용
        """
        response = self.client.post(self.url, {'username': self.username, 'password': self.username})
        self.assertEqual(400, response.status_code)

    def test_unique_username_validation(self):
        """"
        로그인 - 정상 로그인
        """
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue('auth_token' in json.loads(response.content))

    def test_authentication_with_valid_data_not_active_user(self):
        """
        로그인 - 정상 로그인 + 비활성화 유저
        """
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(400, response.status_code)


class UserLogoutAPIViewTestCase(APITestCase):
    login_url = reverse('users:login')
    url = reverse('users:logout')

    def setUp(self):
        """
        셋업 - 유저 생성 + 로그인
        """
        self.user = User.objects.create_user('loginuser', 'loginuser@loginuser.com', 'loginuser123')
        response = self.client.post(self.login_url, {'username': 'loginuser', 'password': 'loginuser123'})
        self.assertEqual(200, response.status_code)
        self.token = Token.objects.last().key

    def test_logout_with_wrong_token(self):
        """
        로그아웃 - 비정상 토큰
        """
        response = self.client.post(self.url, {'auth_token': 'testToken'})
        self.assertEqual(400, response.status_code)

    def test_logout_wtih_valid_data(self):
        """
        로그아웃 - 정상 토큰
        """
        response = self.client.post(self.url, {'auth_token': self.token})
        self.assertEqual(204, response.status_code)

    def test_logout_with_not_active_user(self):
        """
        로그아웃 - 정상 토큰 _ 사용자 비활성화
        """
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, {'auth_token': self.token})
        self.assertEqual(400, response.status_code)