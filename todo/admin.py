from django.contrib import admin

from todo.models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "done", "date_created")
    list_filter = ("done", "date_created")


admin.site.register(Todo, TodoAdmin)
