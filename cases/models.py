from django.db import models

class Case(models.Model):
    CASE_TYPE_CHOICES = [
        ('abduction', 'Abduction'),
        ('defilement', 'Defilement'),
        ('neglegence', 'Neglegence'),
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
        # Add more case types as needed
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
        # Add more locations as needed
    ]

    STAGE_OF_CASE_CHOICES = [
        ('defence hearing', 'Defence Hearing'),
        ('withdrawn', 'Withdrawn'),
        ('hearing', 'Hearing'),
        ('judgement', 'Judgement'),
        ('mention', 'Mention'),
        ('rulling', 'Rulling'),
    ]

    case_number = models.CharField(max_length=100, unique=True)
    case_type = models.CharField(max_length=100, choices=CASE_TYPE_CHOICES)
    accused_name = models.CharField(max_length=255)
    accuser_name = models.CharField(max_length=255)
    accuser_phone = models.CharField(max_length=15)
    court_name = models.CharField(max_length=255)  # Court Name field
    court_date = models.DateField()  # DateField for selecting date
    next_court_date = models.DateField()  # Another DateField
    investigating_officer = models.CharField(max_length=255)
    investigating_officer_phone = models.CharField(max_length=15)
    stage_of_case = models.CharField(max_length=50, choices=STAGE_OF_CASE_CHOICES)  # Dropdown for stage of case
    location = models.CharField(max_length=255, choices=LOCATION_CHOICES)
    

    def __str__(self):
        return self.case_number
