from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('cases/', views.case_list, name='case_list'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('case/new/', views.case_create, name='case_create'),
    path('case/<int:pk>/edit/', views.case_update, name='case_update'),
    path('case/<int:pk>/delete/', views.case_delete, name='case_delete'),
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
