from django.db import models
from django.utils.translation import ugettext_lazy as _



# Create your models here.
class RoomChoices(object):
    GENERAL = 1
    SEMIPRIVATE = 2
    PRIVATE = 3


class GenderType(object):
    MALE = 1
    FEMALE = 2


class MARITALSTATUS(object):
    SINGLE = 1
    MARRIED = 2


class Country(models.Model):
    country_name = models.CharField(max_length=100, blank=True, null=True)


class State(models.Model):
    state_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(models.Model):
    city_name = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    class Meta:
        db_table = 'City'
        verbose_name_plural = "Cities"
        ordering = ['city_name']

    def __unicode__(self):
        return self.city_name


class PatientStatus(object):
    ADMIT = 1
    DISCHARGED = 2



class Beds(models.Model):
    BED_CHOICES = (
        (None, 'Select The Bed Choices'),
        (RoomChoices.GENERAL, 'General'),
        (RoomChoices.SEMIPRIVATE, 'SemiPrivate'),
        (RoomChoices.PRIVATE, "Private")
    )
    bed_type = models.PositiveSmallIntegerField(
        choices=BED_CHOICES, null=True, blank=True
    )
    bed_number = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True, null=False)


class Patient(models.Model):
    GENDER_CHOICES = (
        (None, 'Select The Gender Choices'),
        (GenderType.MALE, 'Male'),
        (GenderType.FEMALE, 'Female')
    )
    MARITAL_STATUS_CHOICES = (
        (None, 'Select The Marital Choices'),
        (MARITALSTATUS.SINGLE, 'Single'),
        (MARITALSTATUS.MARRIED, 'Married')
    )
    Patient_Status_Choices = (
        (None, 'Select The Patient Choices'),
        (PatientStatus.ADMIT, 'Admit'),
        (PatientStatus.DISCHARGED, 'Discharged')
    )
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True, blank=True
    )
    patient_status = models.PositiveSmallIntegerField(
        choices=Patient_Status_Choices, null=True, blank=True
    )
    marital_status = models.PositiveSmallIntegerField(
        choices=MARITAL_STATUS_CHOICES, null=True, blank=True
    )
    occupation = models.CharField(
        max_length=80, null=True, blank=True, default=None
    )
    dob = models.DateField(_('Date OF Birth'), null=True, blank=True)
    location_updated_at = models.DateTimeField(
        null=True, blank=True, default=None
    )

    # Details of the user
    email = models.EmailField(
        _('email address'), max_length=255, unique=True, null=True
    )
    mobile = models.CharField(
        _('mobile number'), max_length=12, blank=True, null=True
    )
    address_line1 = models.CharField(
        _('address line1'), max_length=128, null=True, blank=True
    )
    address_line2 = models.CharField(
        _('address line2'), max_length=128, null=True, blank=True
    )
    city = models.ForeignKey(City, null=True, blank=True, default=None, on_delete=models.CASCADE)
    admit_on = models.DateTimeField(blank=True, null=True)
    discharged_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Patient"

    def get_gender(self):
        """
        :return gender as an int
        """
        if self.gender == "MALE":
            return GenderType.MALE
        elif self.gender == "FEMALE":
            return GenderType.FEMALE
        else:
            return None


class Ward(models.Model):
    bed = models.ForeignKey(Beds, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Wardconfig"
