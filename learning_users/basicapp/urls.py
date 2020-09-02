from django.conf.urls import url
from basicapp import views

# Template tagging
app_name = 'basicapp'

urlpatterns = [
    url(r'^register/$', views.register, name = 'register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]
