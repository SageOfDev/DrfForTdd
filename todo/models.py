from django.conf import settings
from django.db import models


class Todo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="작성자", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="제목", max_length=255)
    done = models.BooleanField(verbose_name="성공 여부", default=False)
    date_created = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.name
