from django.db import models
from django.contrib.auth.models import User
from apps.location.models import Region, District, Ward, Village, Neighborhood


# Create your models here.
class Profile(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    designation       = models.CharField(max_length=30, null=False, blank=False, default="MWANANCHI")
    phone             = models.CharField(max_length=20, null=False, blank=False)
    gender            = models.CharField(max_length=10, null=False, blank=False, default="M")
    dob               = models.DateField(null=False, blank=False)
    id_type           = models.CharField(max_length=10, null=False, blank=False)
    id_number         = models.CharField(max_length=50, null=False, blank=False)
    region            = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=False, blank=False)
    district          = models.ForeignKey(District, on_delete=models.DO_NOTHING, null=False, blank=False)
    ward              = models.ForeignKey(Ward, on_delete=models.DO_NOTHING, null=False, blank=False)
    village           = models.ForeignKey(Village, on_delete=models.DO_NOTHING, null=False, blank=False)
    neighborhood      = models.ForeignKey(Neighborhood, on_delete=models.DO_NOTHING, null=False, blank=False)
    physical_address  = models.TextField(null=True, blank=True)
    house_number      = models.CharField(max_length=50, null=False, blank=False)
    work              = models.CharField(max_length=50, null=False, blank=False)
    be_jembe          = models.IntegerField(null=True, blank=True, default=0)
    working_ward      = models.ForeignKey(Ward, on_delete=models.DO_NOTHING, related_name="working_ward", null=True, blank=True)
    working_village   = models.ForeignKey(Village, on_delete=models.DO_NOTHING, related_name="working_village", null=True, blank=True)
    working_shina     = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'dt_profile'
        managed = True