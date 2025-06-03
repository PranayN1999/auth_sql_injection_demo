from django.contrib import admin
from django.urls import path, include
from users import views
from users.views_vuln import bad_login, bad_register   # add bad_register




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += [
    path("bad-register/", bad_register, name="bad_register"),
    path("bad-login/",    bad_login,    name="bad_login"),
]