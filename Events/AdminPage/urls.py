from django.urls import path
from . import views

app_name = 'adminpage'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_event/', views.add_event, name='add_event'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
