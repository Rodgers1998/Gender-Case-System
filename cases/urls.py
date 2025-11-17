from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout, generate_case_pdf, case_analysis, upcoming_cases_by_county, upcoming_cases_by_subcounty

urlpatterns = [
    path('', views.home, name='home'),
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

    # ✅ Updated routes
    path('cases/upcoming/by-county/', upcoming_cases_by_county, name='upcoming_cases_by_county'),
    path('cases/upcoming/by-subcounty/', upcoming_cases_by_subcounty, name='upcoming_cases_by_subcounty'),

    path('cases/dashboard/', views.case_dashboard, name='all_cases_dashboard'),
    path('case/<int:pk>/verify/', views.verify_case, name='verify_case'),

]
