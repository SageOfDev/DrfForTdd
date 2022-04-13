from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = 'Todo-DRF Admin'
    site_title = 'DRF Sample1'
    index_title = 'TODO-DRF FOR TDD'


admin_site = MyAdminSite(name='myadmin')
