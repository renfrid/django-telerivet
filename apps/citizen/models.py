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

    DESIGNATION_OPTIONS = (
        ('MTENDAJI_KATA', 'MTENDAJI KATA'),
        ('MTENDAJI', 'MTENDAJI KIJIJI'),
        ('MWENYEKITI', 'MWENYEKITI'),
        ('MJUMBE', 'MJUMBE'),
        ('MWANANCHI', 'MWANANCHI'),
    )

    designation       = models.CharField(max_length=30, choices=DESIGNATION_OPTIONS,null=True, blank=True)
    unique_id         = models.CharField(max_length=30, blank=True, null=True)
    name              = models.CharField(max_length=100, blank=True, null=True)
    phone             = models.CharField(max_length=20, blank=False, null=False, unique = True)
    gender            = models.CharField(max_length=10, choices=GENDER_OPTIONS, blank=True, null=True)
    dob               = models.DateField(null=True, blank=True)
    id_type           = models.CharField(max_length=50, choices=ID_TYPE_OPTIONS, blank=True, null=True)
    id_number         = models.CharField(max_length=50, blank=True, null=True)
    ward              = models.ForeignKey(Ward, related_name="ward", on_delete=models.SET_NULL, blank=True, null=True)
    village           = models.ForeignKey(Village, related_name="village", on_delete=models.SET_NULL, blank=True, null=True)
    neighborhood      = models.ForeignKey(Neighborhood, related_name="neighborhood", on_delete=models.SET_NULL, blank=True, null=True)
    shina             = models.CharField(max_length=50, null=True, blank=True)
    hamlet            = models.CharField(max_length=150, blank=True, null=True)
    physical_address  = models.TextField(null=True, blank=True)
    work              = models.CharField(max_length=50, blank=True, null=True)
    be_jembe          = models.IntegerField(null=True, blank=True, default=0)
    chosen            = models.IntegerField(null=True, blank=True, default=0)
    be_jembe_at       = models.DateTimeField(null=True, blank=True)
    be_jembe_by       = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="jembe_user", null=True, blank=True)
    verified_jembe    = models.IntegerField(null=True, blank=True, default=0)
    verified_jembe_at = models.DateTimeField(null=True, blank=True)
    verified_jembe_by = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="verified_jembe_user", null=True, blank=True)
    password          = models.CharField(max_length=20, blank=True, null=True)
    step              = models.IntegerField(default=1, blank=True, null=True)
    status            = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='PENDING', blank=True, null=True)
    is_active         = models.IntegerField(default=0, blank=True, null=True)
    verified_at       = models.DateTimeField(null=True, blank=True)
    verified_by       = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="citizen_verify", null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_by        = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='citizen_user', blank=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table     = 'dt_citizens'
        managed      = True
        verbose_name = 'Citizen'
        verbose_name_plural = 'Citizens'

    def __str__(self):
        return str(self.name)


class CitizenComment(models.Model):
    COMMENT_TYPES_OPTIONS = (
        ("SIRI", 'Siri'),
        ("WAZI", 'Wazi'),
    )

    citizen      = models.ForeignKey(Citizen, related_name="citizen_comment", on_delete=models.CASCADE, blank=False, null=False)
    type         = models.CharField(max_length=50, choices=COMMENT_TYPES_OPTIONS, blank=False, null=False) 
    comments     = models.TextField(null=False, blank=False)
    created_by   = models.ForeignKey(Citizen, related_name="creator", on_delete=models.SET_NULL, blank=True, null=True) 
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table     = 'dt_citizen_comments'
        managed      = True
        verbose_name = 'Citizen Comment'
        verbose_name_plural = 'Citizens Comments'

    def __str__(self):
        return str(self.name)




class Token(models.Model):
    verifier = models.ForeignKey(Citizen, related_name="verifier", on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Citizen, related_name="client", on_delete=models.CASCADE, blank=True, null=True)
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