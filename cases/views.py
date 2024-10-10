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
            Q(court_name__icontains=query) |  # Added field for Court Name
            Q(stage_of_case__icontains=query) |  # Added field for Stage of Case
            Q(ward__icontains=query) |  # Added field for Ward
            Q(police_station__icontains=query)  # Added field for Police Station
        )

    # Limit to the top 5 upcoming cases after filtering
    upcoming_cases = upcoming_cases[:5]

    # Render the home template with the filtered upcoming cases
    return render(request, 'cases/home.html', {'upcoming_cases': upcoming_cases})

@login_required
def case_list(request):
    query = request.GET.get('q')

    # Initialize the variable to an empty queryset to avoid UnboundLocalError
    all_cases = Case.objects.none()

    if request.user.is_superuser:
        # Admin (superuser) can view all cases, including those with past court dates
        all_cases = Case.objects.all().order_by('next_court_date')
    else:
        # Normal user can only see their own cases, including past court dates
        all_cases = Case.objects.filter(user=request.user).order_by('next_court_date')

    # If a search query is provided, filter based on it
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
            Q(court_name__icontains=query) |  # Added field for Court Name
            Q(stage_of_case__icontains=query) |  # Added field for Stage of Case
            Q(ward__icontains=query) |  # Added field for Ward
            Q(police_station__icontains=query)  # Added field for Police Station
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
            case.save()  # Now save the case to the database
            return redirect('case_list')  # Redirect to the case list or another view
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
    # Retrieve case details from the database
    case = Case.objects.get(pk=case_id)

    # Get the logged-in user (case officer)
    case_officer = request.user.username  # Get the username of the logged-in user
    
    # Create a response with the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="case_{case_id}.pdf"'

    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add SHOFCO Logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'images/shofco.png')  # Adjust the path based on your structure
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 100, height - 100, width=2*inch, height=0.75*inch)  # Adjust the position and size

    # Set the title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, height - 150, "Case Detail")

    # Set up the table for displaying case details in a structured format
    case_details = [
        ["Case Number:", case.case_number],
        ["Court File Number:", case.court_file_number],
        ["Case Type:", case.case_type],
        ["Accused Name:", case.accused_name],
        ["Accuser Name:", case.accuser_name],
        ["Accuser Phone:", case.accuser_phone],
        ["Court Name:", case.court_name],
        ["Court Date:", str(case.court_date)],
        ["Next Court Date:", str(case.next_court_date)],
        ["Police Station:", case.police_station],
        ["Investigating Officer:", case.investigating_officer],
        ["Investigating Officer Phone No:", case.investigating_officer_phone],
        ["Stage of Case:", case.get_stage_of_case_display()],
        ["Location:", case.location],
        ["Ward:", case.ward],
    ]

    # Convert the case details into a table format
    table = Table(case_details, colWidths=[2.5 * inch, 4 * inch])  # Adjust column widths

    # Add styling to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font for header
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding below header
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Alternate row background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ]))

    # Draw the table on the PDF
    table.wrapOn(p, width, height)
    table.drawOn(p, 100, height - 400)  # Adjust the position of the table

    # Add case officer information
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 430, f"Case Officer: {case_officer}")
    p.drawString(300, height - 430, "Sign: ______________________")
   
    p.drawString(300, height - 500, "Stamp: ")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response

    # p.drawString(100, y, f"Case Officer: {case_officer}     Sign: _____________     Stamp: __________")
    
    # # Finalize the PDF
    # p.showPage()
    # p.save()

    # return response

