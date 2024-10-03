from django.shortcuts import render, get_object_or_404, redirect
from .models import Case
from .forms import CaseForm
from datetime import date
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def home(request):
    query = request.GET.get('q')
    
    # Filter for upcoming cases based on the next_court_date
    upcoming_cases = Case.objects.filter(next_court_date__gte=date.today()).order_by('next_court_date')[:5]

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
            Q(stage_of_case__icontains=query)  # Added field for Stage of Case
        )

    # Render the home template with upcoming cases
    return render(request, 'cases/home.html', {'upcoming_cases': upcoming_cases})



def case_list(request):
    query = request.GET.get('q')
    cases = Case.objects.all()

    if query:
        cases = cases.filter(
            Q(case_number__icontains=query) |
            Q(case_type__icontains=query) |
            Q(accused_name__icontains=query) |
            Q(accuser_name__icontains=query) |
            Q(accuser_phone__icontains=query) |
            Q(investigating_officer__icontains=query) |
            Q(investigating_officer_phone__icontains=query) |
            Q(location__icontains=query) |
            Q(court_name__icontains=query) |  # Added field for Court Name
            Q(stage_of_case__icontains=query)  # Added field for Stage of Case
        )

    return render(request, 'cases/case_list.html', {'cases': cases})


def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})


def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
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
