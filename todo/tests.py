import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from todo.models import Todo
from todo.serializers import TodoSerializer


class TodoModelTestCase(APITestCase):
    """
    모델 검증
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='model_tester', email='model_tester@test.com')
        cls.todo = Todo.objects.create(owner=cls.user, name='todo title')

    def test_owner_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('owner').verbose_name
        self.assertEquals(field_label, '작성자')

    def test_name_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('name').verbose_name
        self.assertEquals(field_label, '제목')

    def test_done_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('done').verbose_name
        self.assertEquals(field_label, '성공 여부')

    def test_date_created_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, '생성 날짜')

    def test_name_max_length(self):
        todo = Todo.objects.get(id=1)
        max_length = todo._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def tost_todo_str(self):
        self.assertTrue(isinstance(self.todo, Todo))
        self.assertEquals(self.todo.__str__(), self.todo.name)


class TodoListCreateAPIViewTestCase(APITestCase):
    """
    _Todo 생성 및 리스트
    """
    url = reverse('todo:list')

    def setUp(self):
        """
        셋업 - 유저 및 토큰 생성
        """
        self.username = 'tester'
        self.email = 'tester@test.com'
        self.password = "abcde00**"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_todo(self):
        """
        _Todo 생성
        """
        response = self.client.post(self.url, {'name': '샘플2 만들기'})
        self.assertEqual(201, response.status_code)

    def test_user_todos(self):
        """
        리스트 갯수
        """
        Todo.objects.create(owner=self.user, name="샘플TODO 만들기")
        response = self.client.get(self.url)
        self.assertEquals(len(json.loads(response.content)), Todo.objects.count())


class TodoDetaliAPIViewTestCase(APITestCase):
    """
    _Todo - CRUD
    """
    def setUp(self):
        self.username = "tester"
        self.email = "tester@test.com"
        self.password = "abcde00**"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.todo = Todo.objects.create(owner=self.user, name="샘플2 만들기")
        self.url = reverse('todo:detail', kwargs={'pk': self.todo.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication(self.token.key)

    def api_authentication(self, token_key):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    def test_todo_objecct_bundle(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        todo_serializer_data = TodoSerializer(instance=self.todo).data
        response_data = json.loads(response.content)
        self.assertEqual(todo_serializer_data, response_data)

    def test_todo_object_update_authorization(self):
        new_user = User.objects.create_user('tester2', self.email, self.password)
        new_token = Token.objects.create(user=new_user)
        self.api_authentication(new_token.key)

        # PUT all data
        response = self.client.put(self.url, {'name': 'another tester', 'done': True})
        self.assertEqual(403, response.status_code)

        # PATCH
        response = self.client.patch(self.url, {'name': 'another tester'})
        self.assertEqual(403, response.status_code)

    def test_todo_object_update(self):
        response = self.client.put(self.url, {'name': '힘내기 ^^'})
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get('name'), todo.name)

    def test_todo_object_partail_update(self):
        response = self.client.patch(self.url, {'done': True})
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get('done'), todo.done)

    def test_todo_object_delete_authorization(self):
        new_user = User.objects.create_user('tester2', self.email, self.password)
        new_token = Token.objects.create(user=new_user)
        self.api_authentication(new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_todo_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
