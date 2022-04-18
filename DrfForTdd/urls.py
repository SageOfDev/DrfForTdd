from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from docs.views import schema_view

admin.site.site_header = 'Todo-DRF Admin'
admin.site.site_title = 'DRF Sample'
admin.site.index_title = 'TODO-DRF FOR TDD'

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # api
    path('users/', include('users.urls')),
    path('todo/', include('todo.urls')),

    # api_docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # debug_toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]
