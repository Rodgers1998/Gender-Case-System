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
from datetime import date
from django.db.models.functions import TruncMonth
from collections import defaultdict
import os, json

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


@login_required
def home(request):
    query = request.GET.get('q')
    today = date.today()

    # Only show court cases
    filter_base = {
        'is_the_case_proceeding_to_court': True,
        'date_of_court_followup__gte': today
    }
    if request.user.is_superuser:
        upcoming_cases = Case.objects.filter(**filter_base).order_by('date_of_court_followup')
    else:
        upcoming_cases = Case.objects.filter(user=request.user, **filter_base).order_by('date_of_court_followup')

    if query:
        upcoming_cases = upcoming_cases.filter(
            Q(previous_case_number__icontains=query) |
            Q(assault_type__icontains=query) |
            Q(stage_of_case_in_court__icontains=query) |
            Q(site__icontains=query) |
            Q(gender_site_code_of_reporting__icontains=query)
        )

    upcoming_cases = upcoming_cases[:10]
    female_count = Case.objects.filter(survivor_gender__iexact='female').count()
    male_count = Case.objects.filter(survivor_gender__iexact='male').count()

    return render(request, 'cases/home.html', {
        'upcoming_cases': upcoming_cases,
        'female_count': female_count,
        'male_count': male_count,
        'today': today,
    })


@login_required
def case_list(request):
    query = request.GET.get('q')
    county = request.GET.get('county')
    status = request.GET.get('status')

    # All cases including non-court
    cases = Case.objects.all() if request.user.is_superuser else Case.objects.filter(user=request.user)

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

    metrics = {
        'total': cases.count(),
        'closed': cases.filter(case_is_closed=True).count(),
        'in_court': cases.filter(case_still_in_court=True).count(),
        'female': cases.filter(survivor_gender__iexact='female').count(),
    }

    counties = Case.objects.values_list('county', flat=True).distinct().order_by('county')

    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'counties': counties,
        'metrics': metrics
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


@login_required
def case_analysis(request):
    base_qs = Case.objects.filter(is_the_case_proceeding_to_court=True)

    total = base_qs.count()
    closed = base_qs.filter(case_is_closed=True).count()
    in_court = base_qs.filter(case_still_in_court=True).count()
    female = base_qs.filter(survivor_gender__iexact='female').count()
    male = base_qs.filter(survivor_gender__iexact='male').count()

    gender_data = {'labels': ['Female', 'Male'], 'data': [female, male]}

    county_qs = base_qs.values('county').annotate(total=Count('id')).order_by('-total')
    county_data = {
        'labels': [entry['county'] or 'Unknown' for entry in county_qs],
        'data': [entry['total'] for entry in county_qs]
    }

    subcounty_qs = base_qs.values('county', 'case_constituency_name').annotate(total=Count('id')).order_by('county')
    subcounty_data = defaultdict(list)
    for entry in subcounty_qs:
        subcounty_data[entry['county'] or 'Unknown'].append({
            'subcounty': entry['case_constituency_name'] or 'Unknown',
            'total': entry['total']
        })

    monthly_qs = (
        base_qs.annotate(month=TruncMonth('date_of_case_reporting'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    time_series = {
        'labels': [entry['month'].strftime('%b %Y') for entry in monthly_qs if entry['month']],
        'data': [entry['count'] for entry in monthly_qs if entry['month']]
    }

    assault_qs = base_qs.values('county', 'assault_type').annotate(total=Count('id'))
    assault_data = defaultdict(lambda: defaultdict(int))
    assault_types = set()
    for entry in assault_qs:
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
            }
            for assault in sorted(assault_types)
        ]
    }

    context = {
        'kpis': {'total': total, 'closed': closed, 'in_court': in_court, 'female': female, 'male': male},
        'gender_data_json': json.dumps(gender_data),
        'county_data_json': json.dumps(county_data),
        'subcounty_data_json': json.dumps({k: v for k, v in subcounty_data.items()}),
        'time_series_json': json.dumps(time_series),
        'assault_stacked_json': json.dumps(assault_stacked),
    }

    return render(request, 'cases/case_analysis.html', context)


@login_required
def upcoming_cases_by_county(request):
    counties_with_upcoming = (
        Case.objects
        .filter(is_the_case_proceeding_to_court=True, date_of_court_followup__gte=date.today())
        .exclude(county__isnull=True)
        .values('county')
        .annotate(soonest_date=Min('date_of_court_followup'))
        .order_by('soonest_date')
    )

    cases_by_county = {}
    for entry in counties_with_upcoming:
        county = entry['county']
        cases = (
            Case.objects
            .filter(
                is_the_case_proceeding_to_court=True,
                county=county,
                date_of_court_followup__gte=date.today()
            )
            .order_by('date_of_court_followup')[:5]
        )
        cases_by_county[county] = cases

    return render(request, 'cases/upcoming_cases_by_county.html', {'cases_by_county': cases_by_county})


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


@login_required
def case_dashboard(request):
    from collections import defaultdict
    import json
    from django.db.models import Count
    from django.db.models.functions import TruncMonth

    all_cases = Case.objects.all()
    total = all_cases.count()
    closed = all_cases.filter(case_is_closed=True).count()
    in_court = all_cases.filter(case_still_in_court=True).count()
    female = all_cases.filter(survivor_gender__iexact='female').count()
    male = all_cases.filter(survivor_gender__iexact='male').count()

    # KPIs
    kpis = {
        'total': total, 'closed': closed,
        'in_court': in_court, 'female': female, 'male': male
    }

    # Gender Pie
    gender_data = {'labels': ['Female', 'Male'], 'data': [female, male]}

    # Age Group
    age_group = all_cases.values('age_group').annotate(total=Count('id')).order_by('-total')
    age_group_data = {
        'labels': [a['age_group'] or 'Unknown' for a in age_group],
        'data': [a['total'] for a in age_group]
    }

    # Referral Pie
    referral_map = {
        'Medical': 'referred_for_medical_intervention',
        'Police': 'referred_to_police',
        'Counseling': 'referred_to_counseling_and_support',
        'Safe House': 'referred_to_safe_house',
        'DCO': 'referred_to_dco'
    }
    referral_data = {
        'labels': list(referral_map.keys()),
        'data': [all_cases.filter(**{field: True}).count() for field in referral_map.values()]
    }

    # County/Subcounty
    county_data = all_cases.values('county').annotate(total=Count('id')).order_by('-total')
    county_data_json = {
        'labels': [entry['county'] or 'Unknown' for entry in county_data],
        'data': [entry['total'] for entry in county_data]
    }

    subcounty_data = all_cases.values('case_constituency_name').annotate(total=Count('id')).order_by('-total')
    subcounty_data_json = {
        'labels': [entry['case_constituency_name'] or 'Unknown' for entry in subcounty_data],
        'data': [entry['total'] for entry in subcounty_data]
    }

    # Monthly
    time_series = all_cases.annotate(month=TruncMonth('date_of_case_reporting')).values('month').annotate(count=Count('id')).order_by('month')
    time_series_json = {
        'labels': [entry['month'].strftime('%b %Y') for entry in time_series if entry['month']],
        'data': [entry['count'] for entry in time_series if entry['month']]
    }

    # Assault by County (Stacked)
    assault_raw = all_cases.values('county', 'assault_type').annotate(total=Count('id'))
    assault_data = defaultdict(lambda: defaultdict(int))
    assault_types = set()

    for entry in assault_raw:
        county = entry['county'] or 'Unknown'
        assault = entry['assault_type'] or 'Unknown'
        assault_data[assault][county] += entry['total']
        assault_types.add(assault)

    counties = sorted({c for counts in assault_data.values() for c in counts})
    assault_stacked = {
        'labels': counties,
        'datasets': [
            {
                'label': assault,
                'data': [assault_data[assault].get(c, 0) for c in counties]
            } for assault in sorted(assault_types)
        ]
    }

    # Referral by County (Stacked)
    referral_stacked = {
        'labels': counties,
        'datasets': [
            {
                'label': label,
                'data': [
                    all_cases.filter(county=c, **{field: True}).count() for c in counties
                ]
            } for label, field in referral_map.items()
        ]
    }

    context = {
        'kpis': kpis,
        'gender_data': gender_data,
        'age_group_data': age_group_data,
        'referral_data': referral_data,
        'county_data': county_data_json,
        'subcounty_data': subcounty_data_json,
        'time_series': time_series_json,
        'assault_stacked': assault_stacked,
        'referral_stacked': referral_stacked,
    }
    return render(request, 'cases/all_cases_dashboard.html', context)

