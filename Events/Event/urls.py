from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Event'

urlpatterns = [
    path('', views.login_view, name='landing'),
    path('list/', views.event_list, name='event_list'),
    path('join/<int:event_id>/', views.join_event, name='join_event'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout_view, name='logout')
]
