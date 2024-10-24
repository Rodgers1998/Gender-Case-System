from django.shortcuts import render, get_object_or_404, redirect
from .models import Case
from .forms import CaseForm
from datetime import date
from django.db.models import Q
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse

from django.shortcuts import render
from django.db.models import Count
from .models import Case



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    logout(request)  # Log the user out
    return render(request, 'cases/logout.html')  # Render your custom logout template

@login_required
def home(request):
    query = request.GET.get('q')

    # Filter for upcoming cases based on the next_court_date
    if request.user.is_superuser:
        # Admin (superuser) can view all upcoming cases
        upcoming_cases = Case.objects.filter(next_court_date__gte=date.today()).order_by('next_court_date')
    else:
        # Normal user can only see their own upcoming cases
        upcoming_cases = Case.objects.filter(user=request.user, next_court_date__gte=date.today()).order_by('next_court_date')

    # If a search query is provided, filter the upcoming cases based on it
    if query:
        upcoming_cases = upcoming_cases.filter(
            Q(case_number__icontains=query) |
            Q(case_type__icontains=query) |
            Q(accused_name__icontains=query) |
            Q(accuser_name__icontains=query) |
            Q(accuser_phone__icontains=query) |
            Q(investigating_officer__icontains=query) |
            Q(investigating_officer_phone__icontains=query) |
            Q(location__icontains=query) |
            Q(court_name__icontains=query) |
            Q(stage_of_case__icontains=query) |
            Q(ward__icontains=query) |
            Q(police_station__icontains=query) |
            Q(county__icontains=query) |          # Added county
            Q(sub_county__icontains=query)        # Added sub-county
        )


    # Limit to the top 10 upcoming cases after filtering
    upcoming_cases = upcoming_cases[:10]  # Change from 5 to 10

    # Render the home template with the filtered upcoming cases
    return render(request, 'cases/home.html', {'upcoming_cases': upcoming_cases})


@login_required
def case_list(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('filter')  # To determine if 'today' filter is active

    # Initialize the variable to an empty queryset to avoid UnboundLocalError
    all_cases = Case.objects.none()

    if request.user.is_superuser:
        # Admin (superuser) can view all cases
        all_cases = Case.objects.all().order_by('next_court_date')
    else:
        # Normal user can only see their own cases
        all_cases = Case.objects.filter(user=request.user).order_by('next_court_date')

    # Filter for today's cases
    if filter_type == 'today':
        today = date.today()
        all_cases = all_cases.filter(case_registration_date=today)  # Use case_registration_date to filter today's cases

    # If a search query is provided, filter the results based on it
    if query:
        all_cases = all_cases.filter(
            Q(case_number__icontains=query) |
            Q(case_type__icontains=query) |
            Q(accused_name__icontains=query) |
            Q(accuser_name__icontains=query) |
            Q(accuser_phone__icontains=query) |
            Q(investigating_officer__icontains=query) |
            Q(investigating_officer_phone__icontains=query) |
            Q(location__icontains=query) |
            Q(court_name__icontains=query) |
            Q(stage_of_case__icontains=query) |
            Q(ward__icontains=query) |
            Q(police_station__icontains=query) |
            Q(county__icontains=query) |          # Filter by county
            Q(sub_county__icontains=query)        # Filter by sub-county
        )

    # Pagination - Show 10 cases per page
    paginator = Paginator(all_cases, 10)
    page_number = request.GET.get('page')
    cases = paginator.get_page(page_number)

    # Render the case list template with all cases
    return render(request, 'cases/case_list.html', {'cases': cases})




def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})

@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)  # Don't save to the database yet
            case.user = request.user  # Assign the current logged-in user
            case.case_registration_date = date.today()  # Manually set the case registration date to today
            case.save()  # Save the case to the database
            return redirect('case_list')
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form': form})

def case_update(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/case_form.html', {'form': form})

def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'cases/case_confirm_delete.html', {'case': case})



@login_required
def case_analysis(request):
    # Get case counts by county
    county_data = Case.objects.values('county').annotate(total=Count('id')).order_by('-total')

    # Get case counts by sub-county and case type
    subcounty_data = Case.objects.values('county', 'sub_county', 'case_type').annotate(total=Count('id')).order_by('county', 'sub_county')

    # Pass the data to the template
    return render(request, 'cases/case_analysis.html', {
        'county_data': county_data,
        'subcounty_data': subcounty_data,
    })



@login_required
def upcoming_cases_by_county(request):
    # Define the counties to filter by
    counties = ['Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita-Taveta']

    # Dictionary to store the top 5 cases for each county
    cases_by_county = {}

    # Fetch top 5 upcoming cases per county
    for county in counties:
        cases = Case.objects.filter(
            county__iexact=county,
            next_court_date__gte=date.today()
        ).order_by('next_court_date')[:5]  # Top 5 upcoming cases per county
        cases_by_county[county] = cases

    return render(request, 'cases/upcoming_cases_by_county.html', {'cases_by_county': cases_by_county})





import os
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from .models import Case  # Adjust based on your model's location


def generate_case_pdf(request, case_id):
    case = Case.objects.get(pk=case_id)
    case_officer = request.user.username

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="case_{case_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add logo (if available)
    logo_path = os.path.join(settings.STATIC_ROOT, 'images/shofco.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 100, height - 100, width=2 * inch, height=0.75 * inch)

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, height - 150, "Case Detail")

    # Case Details Formatting
    p.setFont("Helvetica", 12)
    line_height = 14  # Adjust spacing between lines
    y_position = height - 180  # Initial y-position for content

    # Helper function to draw label and value like in case_detail.html
    def draw_detail(label, value):
        nonlocal y_position
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y_position, f"{label}:")
        p.setFont("Helvetica", 12)
        p.drawString(250, y_position, str(value) if value else "N/A")  # Handles None values gracefully
        y_position -= line_height

    # Render each case detail
    draw_detail("Case Number", case.case_number)
    draw_detail("Court File Number", case.court_file_number)
    draw_detail("Case Type", case.case_type)
    draw_detail("Accused Name", case.accused_name)
    draw_detail("Accuser Name", case.accuser_name)
    draw_detail("Accuser Phone", case.accuser_phone)
    draw_detail("Court Name", case.court_name)
    draw_detail("Court Date", case.court_date)
    draw_detail("Next Court Date", case.next_court_date)
    draw_detail("Police Station", case.police_station)
    draw_detail("Investigating Officer", case.investigating_officer)
    draw_detail("IO Phone No", case.investigating_officer_phone)
    draw_detail("Stage of Case", case.get_stage_of_case_display())
    draw_detail("County", case.county)
    draw_detail("Sub-County", case.sub_county)
    draw_detail("Location", case.location)
    draw_detail("Ward", case.ward)
    

    # Case Officer and Signatures
    y_position -= 30  # Add space before signatures
    p.drawString(100, y_position, f"Case Officer: {case_officer}")
    p.drawString(300, y_position, "Sign: ______________________")
    y_position -= 70  # Adjust space for Stamp
    p.drawString(300, y_position, "Stamp: ")

    # Finalize PDF
    p.showPage()
    p.save()

    return response
