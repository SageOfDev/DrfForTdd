from django.conf import settings
from django.urls import path, include, re_path

from DrfForTdd.admin import admin_site
from docs.views import schema_view

urlpatterns = [
    # admin
    path('admin/', admin_site.urls),

    # api
    path('users/', include('users.urls')),
    path('todo/', include('todo.urls')),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # api_docs
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        # debug_toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]