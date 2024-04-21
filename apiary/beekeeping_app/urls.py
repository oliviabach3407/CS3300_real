from django.urls import path, include
#BUG FIX
from django.contrib.auth import views as auth_views
from . import views

#for image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #other patterns
    path('', views.index, name='index'),
    path('keeper/', views.keeperView, name='keeper'),

    #authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name = 'register_page'),
    path('user/', views.userPage, name='user_page'),
    path('logout/', views.logoutView, name='logout'),

    #reverse paths
    path('apiary/<int:apiary>/', views.apiaryDetail, name='apiary-detail'),
    path('keeper/<int:keeper>/', views.keeperDetail, name='keeper-detail'),
    path('hive/<int:hive>/', views.hiveDetail, name='hive-detail'),

    #create, view, update, delete hives
    path('hive/<int:apiary_id>/create-hive/', views.newHive, name='create-hive'),
    path('hive/<int:apiary>/update-hive/<int:hive>/', views.updateHive, name='update-hive'),
    path('hive/<int:apiary>/delete-hive/<int:hive>/', views.deleteHive, name='delete-hive'),

    #update apiary 
    path('keeper/<int:keeper>/update-apiary/<int:apiary>/', views.updateApiary, name='update-apiary'),

    #calendar??
    path('hive/<int:hive_id>/edit-calendar/', views.editCalendar, name='edit-calendar'),
    path('hive/<int:hive_id>/calendar/', views.calendarView, name='calendar'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
