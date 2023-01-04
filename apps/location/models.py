from django.db import models

# Create your models here.

#regions
class Region(models.Model):
    name      = models.CharField(max_length=30, blank = False, null = False)
    post_code = models.CharField(max_length=2, blank = True, null = True)

    class Meta:
        db_table     = 'dt_regions'
        managed      = True
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return str(self.name)

#districts
class District(models.Model):
    view_id   =  models.CharField(max_length=10, blank = True, null = True)
    name      = models.CharField(max_length=30, blank = False, null = False)
    region    = models.ForeignKey(Region, related_name='region', on_delete=models.DO_NOTHING)
    post_code = models.CharField(max_length=4, blank = True, null = True)
    phone     = models.CharField(max_length=20, blank = True, null = True)

    class Meta: 
        db_table = 'dt_districts'
        managed  = True
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def __str__(self):
        return str(self.name)

#wards
class Ward(models.Model):
    view_id   =  models.CharField(max_length=10, blank = True, null = True)
    name      = models.CharField(max_length=30,blank=False, null=False)
    district  = models.ForeignKey(District, related_name='district',on_delete=models.DO_NOTHING) 
    post_code = models.CharField(max_length=4, blank = True, null = True)     

    class Meta: 
        db_table  =  'dt_wards'
        managed   =  True
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'  

    def __str__(self):
        return str(self.name)


class Village(models.Model):
    view_id      =  models.CharField(max_length=10, blank = True, null = True)
    name         = models.CharField(max_length=30, null=False, blank=False)
    ward         = models.ForeignKey(Ward, related_name='village', on_delete=models.DO_NOTHING)
    post_code    = models.CharField(max_length=6, blank = True, null = True)

    class Meta:
        db_table = 'dt_villages'
        managed  = True
        verbose_name  = 'Village'
        verbose_name_plural = 'Villages'  

    def __str__(self):
        return str(self.name)   


class Neighborhood(models.Model):
    view_id      =  models.CharField(max_length=10, blank = True, null = True)
    name         = models.CharField(max_length=30, null=False, blank=False)
    village      = models.ForeignKey(Village, related_name='neighborhood', on_delete=models.DO_NOTHING)
    post_code    = models.CharField(max_length=6, blank = True, null = True)

    class Meta:
        db_table  = 'dt_neighborhood'
        managed   = True
        verbose_name = 'Neighborhood'

    def __str__(self):
        return str(self.name) 