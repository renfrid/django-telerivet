from django.db import models
from django.contrib.auth.models import User
from apps.location.models import Village

# Create your models here.
class Citizen(models.Model):
    GENDER_OPTIONS = (
        ('Mme', 'Mme'),
        ('Mke', 'Mke'),
    )

    ID_TYPE_OPTIONS = (
        ('NIDA', 'NIDA'),
        ('Leseni ya udereva', 'Leseni ya udereva'),
        ('Passport', 'Passport'),
        ('Kitambulisho cha mpiga kura', 'Kitambulisho cha mpiga kura'),
        ('Sina Kitambulisho', 'Sina Kitambulisho'),
    )

    name            = models.CharField(max_length=100, blank=True, null=True)
    phone           = models.CharField(max_length=20, blank=True, null=True)
    gender          = models.CharField(max_length=10, choices=GENDER_OPTIONS,default='Mme')
    dob             = models.CharField(max_length=20, blank=True, null=True)
    id_type         = models.CharField(max_length=50, choices=ID_TYPE_OPTIONS,default='NIDA')
    id_number       = models.CharField(max_length=50, blank=False, null=False)
    village         = models.ForeignKey(Village, on_delete=models.DO_NOTHING, null=True, blank=True)
    hamlet          = models.CharField(max_length=50, blank=False, null=False)
    house_number    = models.CharField(max_length=50, blank=False, null=False)
    work            = models.CharField(max_length=100, blank=True, null=True)
    password        = models.CharField(max_length=20, blank=False, null=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_by      = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user', blank=True, null=True)
    updated_at      = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table     = 'dt_citizens'
        managed      = True
        verbose_name = 'Citizen'
        verbose_name_plural = 'Citizens'

    def __str__(self):
        return str(self.name)