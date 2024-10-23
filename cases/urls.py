from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout 

from .views import generate_case_pdf
from .views import case_analysis

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('cases/', views.case_list, name='case_list'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('case/new/', views.case_create, name='case_create'),
    path('case/<int:pk>/edit/', views.case_update, name='case_update'),
    path('case/<int:pk>/delete/', views.case_delete, name='case_delete'),
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    
    path('case/<int:case_id>/pdf/', generate_case_pdf, name='case_pdf'),
    path('case_analysis/', case_analysis, name='case_analysis'),
    
]
