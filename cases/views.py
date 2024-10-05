from django.shortcuts import render, get_object_or_404, redirect
from .models import Case
from .forms import CaseForm
from datetime import date
from django.db.models import Q
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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

    # Initialize the variable to avoid UnboundLocalError
    all_cases = None

    if request.user.is_superuser:
        # Admin (superuser) can view all cases, including those with past court dates
        all_cases = Case.objects.all().order_by('next_court_date')
    else:
        # Normal user can only see their own cases, including past court dates
        all_cases = Case.objects.filter(user=request.user).order_by('next_court_date')

    # If a search query is provided, filter based on it
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

    # Pagination - Show 10 cases per page
    paginator = Paginator(all_cases, 10)  # Ensure all_cases is passed here
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
