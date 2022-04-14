from django.urls import path

from todo.views import TodoListCreateAPIView, TodoDetailAPIView

app_name = 'todo'

urlpatterns = [
    path('', TodoListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', TodoDetailAPIView.as_view(), name='detail'),
]