from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'case_type', 'accused_name','accuser_name', 'accuser_phone', 'court_date', 'next_court_date', 'investigating_officer','investigating_officer_phone','stage_of_case','county','sub_county', 'location', 'ward' )