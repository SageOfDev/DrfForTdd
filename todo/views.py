from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from todo.serializers import TodoSerializer


class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
