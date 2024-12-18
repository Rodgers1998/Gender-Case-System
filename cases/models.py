from django.db import models
from django.contrib.auth.models import User


class Case(models.Model):
    CASE_TYPE_CHOICES = [
        ('abduction', 'Abduction'),
        ('defilement', 'Defilement'),
        ('neglegence', 'Negligence'),
        ('legal councelling', 'Legal Councelling'),
        ('emotional abuse', 'Emotional Abuse'),
        ('child abuse', 'Child Abuse'),
        ('physical assault', 'Physical Assault'),
        ('domestic violence', 'Violence'),
        ('attempted defilement', 'Attempted Defilement'),
        ('sodomy', 'Sodomy'),
        ('rape', 'Rape'),
        ('juvenile deliquency', 'Juvenile Deliquency'),
        ('attempted sodomy', 'Attempted Sodomy'),
        ('attempted rape', 'Attempted Rape'),
        ('sexual assault', 'Sexual Assault'),
        ('indicent act', 'Incident Act'),
        ('sexual harrassment', 'Sexual Harrassment'),
    ]
    
    COUNTY_CHOICES = [
        ('mombasa', 'Mombasa'),
        ('kwale', 'Kwale'),
        ('kilifi', 'Kilifi'),
        ('tana river', 'Tana River'),
        ('lamu', 'Lamu'),
        ('taita-taveta', 'Taita-Taveta'),
    ]
    
    SUB_COUNTY_CHOICES=[
        ('changamwe', ' Changamwe'),
        ('jomvu','Jomvu'),
        ('kisauni','Kisauni'),
        ('likoni','Likoni'),
        ('mvita','Mvita'),
        ('nyali','Nyali'),
        ('matuga','Matuga'),
        ('msambweni','Msambweni'),
        ('lunga lunga','Lunga Lunga'),
        ('kinango','Kinango'),
        ('kilifi north','Kilifi North'),
        ('kilifi south','Kilifi South'),
        ('malindi','Malindi'),
        ('magarini','Magarini'),
        ('rabai','Rabai'),
        ('kaloleni','Kaloleni'),
        ('ganze','Ganze'),
        ('gazole','Galole'),
        ('bura','Bura'),
        ('garsen','Garsen'),
        ('lamu east','Lamu East'),
        ('lamu west','Lamu West'),
        ('mwatate','Mwatate'),
        ('voi','Voi'),
        ('taveta','Taveta'),
        ('wundanyi','Wundanyi'),
    ]

    STAGE_OF_CASE_CHOICES = [
        ('defence hearing', 'Defence Hearing'),
        ('withdrawn', 'Withdrawn'),
        ('hearing', 'Hearing'),
        ('judgement', 'Judgement'),
        ('mention', 'Mention'),
        ('rulling', 'Rulling'),
        ('sentencing', 'Sentencing'),  # Modified to allow custom durations
        ('jailing', 'Jailing'), 
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case_number = models.CharField(max_length=100, unique=True)
    court_file_number = models.CharField(max_length=100, blank=True, null=True)  # Added court file number
    case_type = models.CharField(max_length=100, choices=CASE_TYPE_CHOICES)
    accused_name = models.CharField(max_length=255)
    accuser_name = models.CharField(max_length=255)
    accuser_phone = models.CharField(max_length=15)
    court_name = models.CharField(max_length=255)
    court_date = models.DateField()
    next_court_date = models.DateField()
    police_station = models.CharField(max_length=255, null=True)
    investigating_officer = models.CharField(max_length=255)
    investigating_officer_phone = models.CharField(max_length=15)
    stage_of_case = models.CharField(max_length=100, choices=STAGE_OF_CASE_CHOICES)
    sentence_duration = models.CharField(max_length=255,blank=True, null=True, help_text="Sentencing duration in months or years")  # New field
    jail_duration = models.CharField(max_length=255,blank=True, null=True, help_text="Jail duration in months or years")  # New field
    county= models.CharField(max_length=255, choices=COUNTY_CHOICES, blank=True, null=True)
    sub_county = models.CharField(max_length=255, choices=SUB_COUNTY_CHOICES, blank=True, null=True)  # Added Sub-County field
    location = models.CharField(max_length=255, null=True)

    ward = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.case_number
