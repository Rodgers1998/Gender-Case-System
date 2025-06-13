from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.db.models import Q, Count, Min
from django.core.paginator import Paginator
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from datetime import date

from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Case

from .models import Case
from .forms import CaseForm, UserRegistrationForm


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
    logout(request)
    return render(request, 'cases/logout.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from .models import Case

@login_required
def home(request):
    query = request.GET.get('q')
    today = date.today()

    if request.user.is_superuser:
        upcoming_cases = Case.objects.filter(date_of_court_followup__gte=today).order_by('date_of_court_followup')
    else:
        upcoming_cases = Case.objects.filter(user=request.user, date_of_court_followup__gte=today).order_by('date_of_court_followup')

    if query:
        upcoming_cases = upcoming_cases.filter(
            Q(previous_case_number__icontains=query) |
            Q(assault_type__icontains=query) |
            Q(stage_of_case_in_court__icontains=query) |
            Q(site__icontains=query) |
            Q(gender_site_code_of_reporting__icontains=query)
        )

    upcoming_cases = upcoming_cases[:10]

    # Additional metrics
    female_count = Case.objects.filter(survivor_gender__iexact='female').count()
    male_count = Case.objects.filter(survivor_gender__iexact='male').count()

    context = {
        'upcoming_cases': upcoming_cases,
        'female_count': female_count,
        'male_count': male_count,
        'today': today,
    }

    return render(request, 'cases/home.html', context)



from django.db.models import Q, Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Case

@login_required
def case_list(request):
    query = request.GET.get('q')
    county = request.GET.get('county')
    status = request.GET.get('status')

    # Base queryset
    cases = Case.objects.all() if request.user.is_superuser else Case.objects.filter(user=request.user)

    # Filtering
    if query:
        cases = cases.filter(
            Q(previous_case_number__icontains=query) |
            Q(assault_type__icontains=query) |
            Q(stage_of_case_in_court__icontains=query)
        )
    if county:
        cases = cases.filter(county__iexact=county)
    if status == 'closed':
        cases = cases.filter(case_is_closed=True)
    elif status == 'in_court':
        cases = cases.filter(case_still_in_court=True)

    # Metrics
    total = cases.count()
    closed = cases.filter(case_is_closed=True).count()
    in_court = cases.filter(case_still_in_court=True).count()
    female = cases.filter(survivor_gender__iexact='female').count()

    # Unique counties for filter dropdown
    counties = Case.objects.values_list('county', flat=True).distinct().order_by('county')

    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'counties': counties,
        'metrics': {
            'total': total,
            'closed': closed,
            'in_court': in_court,
            'female': female
        }
    })



@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})


@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            return redirect('case_list')
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form': form})


@login_required
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


@login_required
def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'cases/case_confirm_delete.html', {'case': case})


# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import date
from .models import Case
import json
from collections import defaultdict

@login_required
def case_analysis(request):
    total = Case.objects.count()
    closed = Case.objects.filter(case_is_closed=True).count()
    in_court = Case.objects.filter(case_still_in_court=True).count()
    female = Case.objects.filter(survivor_gender__iexact='female').count()
    male = Case.objects.filter(survivor_gender__iexact='male').count()

    gender_data = {
        'labels': ['Female', 'Male'],
        'data': [female, male]
    }

    county_queryset = Case.objects.values('county').annotate(total=Count('id')).order_by('-total')
    county_data = {
        'labels': [entry['county'] or 'Unknown' for entry in county_queryset],
        'data': [entry['total'] for entry in county_queryset]
    }

    subcounty_queryset = Case.objects.values('county', 'case_constituency_name').annotate(total=Count('id')).order_by('-total')
    subcounty_data = defaultdict(list)
    for entry in subcounty_queryset:
        subcounty_data[entry['county'] or 'Unknown'].append({
            'subcounty': entry['case_constituency_name'] or 'Unknown',
            'total': entry['total']
        })

    time_series_queryset = (
        Case.objects.annotate(month=TruncMonth('date_of_case_reporting'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    time_series = {
        'labels': [entry['month'].strftime('%b %Y') for entry in time_series_queryset if entry['month']],
        'data': [entry['count'] for entry in time_series_queryset if entry['month']]
    }

    assault_queryset = Case.objects.values('county', 'assault_type').annotate(total=Count('id'))
    assault_data = defaultdict(lambda: defaultdict(int))
    assault_types = set()

    for entry in assault_queryset:
        county = entry['county'] or 'Unknown'
        assault = entry['assault_type'] or 'Unknown'
        assault_data[assault][county] += entry['total']
        assault_types.add(assault)

    counties = sorted({county for counts in assault_data.values() for county in counts})
    assault_stacked = {
        'labels': counties,
        'datasets': [
            {
                'label': assault,
                'data': [assault_data[assault].get(county, 0) for county in counties]
            } for assault in sorted(assault_types)
        ]
    }

    context = {
        'kpis': {
            'total': total,
            'closed': closed,
            'in_court': in_court,
            'female': female,
            'male': male,
        },
        'gender_data_json': json.dumps(gender_data),
        'county_data_json': json.dumps(county_data),
        'subcounty_data_json': json.dumps({k: v for k, v in subcounty_data.items()}),
        'time_series_json': json.dumps(time_series),
        'assault_stacked_json': json.dumps(assault_stacked),
    }

    return render(request, 'cases/case_analysis.html', context)





@login_required
def upcoming_cases_by_county(request):
    # Step 1: Get counties with upcoming cases, annotated by their soonest court date
    counties_with_soonest_dates = (
        Case.objects
        .filter(date_of_court_followup__gte=date.today())
        .exclude(county__isnull=True)
        .values('county')
        .annotate(soonest_date=Min('date_of_court_followup'))
        .order_by('soonest_date')  # Sort counties by their earliest court date
    )

    # Step 2: For each county, fetch up to 5 upcoming cases
    cases_by_county = {}
    for entry in counties_with_soonest_dates:
        county = entry['county']
        cases = (
            Case.objects
            .filter(county=county, date_of_court_followup__gte=date.today())
            .order_by('date_of_court_followup')[:5]
        )
        cases_by_county[county] = cases

    return render(request, 'cases/upcoming_cases_by_county.html', {
        'cases_by_county': cases_by_county
    })

@login_required
def generate_case_pdf(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="case_{case_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    border_margin = 30
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.rect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin)

    logo_path = os.path.join(settings.STATIC_ROOT, 'images/shofco.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width / 2 - inch, height - 100, width=2 * inch, height=0.75 * inch)

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 130, "Gender Department Case")
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 160, "Case Detail")

    p.setFont("Helvetica", 12)
    line_height = 14
    y_position = height - 200

    def draw_detail(label, value):
        nonlocal y_position
        p.setFont("Helvetica-Bold", 12)
        p.drawString(border_margin + 10, y_position, f"{label}:")
        p.setFont("Helvetica", 12)
        p.drawString(border_margin + 160, y_position, str(value) if value else "N/A")
        y_position -= line_height

    # Draw fields selectively for brevity (or loop through model._meta.fields for full automation)
    draw_detail("Case ID", case.case_id)
    draw_detail("Assigned To", case.assigned_to)
    draw_detail("Previous Case No.", case.previous_case_number)
    draw_detail("Date of Reporting", case.date_of_case_reporting)
    draw_detail("Date of Intake", case.date_of_case_intake)
    draw_detail("Assault Type", case.assault_type)
    draw_detail("Court Follow-up", case.date_of_court_followup)
    draw_detail("Stage of Case", case.stage_of_case_in_court)
    draw_detail("County", case.county)
    draw_detail("Constituency", case.case_constituency_name)
    draw_detail("Ward", case.case_ward_name)
    draw_detail("Site", case.site)

    y_position -= 30
    p.drawString(border_margin + 10, y_position, f"Case Officer: {request.user.username}")
    p.drawString(width - border_margin - 200, y_position, "Sign: ______________________")
    y_position -= 70
    p.drawString(width - border_margin - 200, y_position, "Stamp: ")

    p.showPage()
    p.save()
    return response
