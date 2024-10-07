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

    LOCATION_CHOICES = [
        ('runyu', 'Runyu'),
        ('miritini', 'Miritini'),
        ('birikani', 'Birikani'),
        ('giriamani', 'Giriamani'),
        ('nairobi area', 'Nairobi Area'),
        ('centre', 'Centre'),
        ('mkupe', 'Mkupe'),
        ('kachimbeni', 'Kachimbani'),
        ('darajani', 'Darajani'),
        ('majengo', 'Majengo'),
        ('kibarani', 'Kibirani'),
        ('kwashee', 'Kwashee'),
        ('ganahola', 'Ganahola'),
        ('aldina', 'Aldina'),
        ('owino huru', 'Owino Huru'),
        ('chamunyu jomvu', 'Chamunyu Jomvu'),
        ('staff', 'Staff'),
        ('jomvu', 'Jomvu'),
        ('majengo mapya', 'Majengo Mapya'),
        ('kwa mwanzia', 'Kwa Mwanzia'),
        ('kilifi south', 'Kilifi South'),
        ('likoni', 'Likoni'),
        ('kisauni', 'Kisauni'),
        ('nyali', 'Nyali'),
        ('changamwe', 'Changamwe'),
        ('kwapunda', 'Kwapunda'),
        ('bahati', 'Bahati'),
    ]

    STAGE_OF_CASE_CHOICES = [
        ('defence hearing', 'Defence Hearing'),
        ('withdrawn', 'Withdrawn'),
        ('hearing', 'Hearing'),
        ('judgement', 'Judgement'),
        ('mention', 'Mention'),
        ('rulling', 'Rulling'),
        ('sentencing_3_years', 'Sentencing for 3 years'),  # Added
        ('jailed_10_years', 'Jailed for 10 years'),  # Added
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
    sub_county = models.CharField(max_length=255, blank=True, null=True)  # Added Sub-County field
    location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    ward = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.case_number
