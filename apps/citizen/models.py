from django.db import models
from django.contrib.auth.models import User
from apps.location.models import Region, Ward, District, Village, Neighborhood

# Create your models here.
class Citizen(models.Model):
    GENDER_OPTIONS = (
        ('M', 'Mme'),
        ('F', 'Mke'),
    )

    ID_TYPE_OPTIONS = (
        ('NIDA', 'NIDA'),
        ('DRIVER LICENCE', 'Leseni ya udereva'),
        ('PASSPORT', 'Passport'),
        ('VOTE ID', 'Kitambulisho cha mpiga kura'),
        ('SINA', 'Sina Kitambulisho'),
    )

    STATUS_OPTIONS = (
        ('PENDING', 'PENDING'),
        ('UNVERIFIED', 'UNVERIFIED'),
        ('VERIFIED', 'VERIFIED'),
        ('PARTIAL', 'PARTIAL'),
        ('COMPLETED', 'COMPLETED'),
        ('VALID', 'VALID'),
        ('INVALID', 'INVALID'),
    )

    designation       = models.CharField(max_length=30, null=True, blank=True)
    unique_id         = models.CharField(max_length=30, blank=True, null=True)
    name              = models.CharField(max_length=100, blank=True, null=True)
    phone             = models.CharField(max_length=20, blank=False, null=False)
    gender            = models.CharField(max_length=10, choices=GENDER_OPTIONS,default='M', blank=True, null=True)
    dob               = models.CharField(max_length=20, blank=True, null=True)
    id_type           = models.CharField(max_length=50, choices=ID_TYPE_OPTIONS,default='NIDA', blank=True, null=True)
    id_number         = models.CharField(max_length=50, blank=True, null=True)
    ward              = models.ForeignKey(Ward, related_name="citizen_ward", on_delete=models.DO_NOTHING, blank=True, null=True)
    village           = models.ForeignKey(Village, related_name="citizen_village", on_delete=models.DO_NOTHING, blank=True, null=True)
    neighborhood      = models.ForeignKey(Neighborhood, related_name="citizen_neighborhood", on_delete=models.DO_NOTHING, blank=True, null=True)
    hamlet            = models.CharField(max_length=150, blank=True, null=True)
    physical_address  = models.TextField(null=True, blank=True)
    work              = models.CharField(max_length=50, blank=True, null=True)
    be_jembe          = models.IntegerField(null=True, blank=True, default=0)
    working_ward      = models.ForeignKey(Ward, on_delete=models.DO_NOTHING, related_name="citizen_working_ward", null=True, blank=True)
    working_village   = models.ForeignKey(Village, on_delete=models.DO_NOTHING, related_name="citizen_working_village", null=True, blank=True)
    working_shina     = models.CharField(max_length=50, null=True, blank=True)
    password          = models.CharField(max_length=20, blank=True, null=True)
    step              = models.IntegerField(default=1, blank=True, null=True)
    status            = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='PENDING', blank=True, null=True)
    is_active         = models.IntegerField(default=0, blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_by        = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='citizen_user', blank=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table     = 'dt_citizens'
        managed      = True
        verbose_name = 'Citizen'
        verbose_name_plural = 'Citizens'

    def __str__(self):
        return str(self.name)


class Token(models.Model):
    citizen = models.ForeignKey(Citizen, related_name="citizen", on_delete=models.DO_NOTHING, blank=False, null=False)
    client = models.ForeignKey(Citizen, related_name="client", on_delete=models.DO_NOTHING, blank=False, null=False)
    otp = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(auto_now=True, null=True)
    status = models.IntegerField(default=0, blank=True, null=True)   

    class Meta:
        db_table     = 'dt_tokens'
        managed      = True
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def __str__(self):
        return str(self.otp)     