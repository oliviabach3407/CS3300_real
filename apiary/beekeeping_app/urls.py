from django.urls import path
#BUG FIX
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # other patterns
    path('', views.index, name='index'),
    path('keeper/', views.keeperView, name='keeper'),

    #BUG FIX
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),

    #reverse paths
    path('apiary/<int:apiary>/', views.apiaryDetail, name='apiary-detail'),
    path('keeper/<int:keeper>/', views.keeperDetail, name='keeper-detail'),
    path('hive/<int:hive>/', views.hiveDetail, name='hive-detail'),

    #create, view, update, delete hives
    path('hive/<int:apiary>/create-hive/', views.newHive, name='create-hive'),
    path('hive/<int:apiary>/update-hive/<int:hive>/', views.updateHive, name='update-hive'),
    path('hive/<int:apiary>/delete-hive/<int:hive>/', views.updateHive, name='delete-hive'),

    #update apiary 
    path('keeper/<int:keeper>/update-apiary/<int:apiary>/', views.updateApiary, name='update-apiary'),
]
