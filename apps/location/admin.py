from django.contrib import admin
from .models import Region, District, Ward, Village, Neighborhood

# Register your models here.
#regions
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_code', 'name']
    search_fields = ['name__startwith']
    ordering = ("name",)

admin.site.register(Region, RegionAdmin)

#districts
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'region', 'phone']
    list_filter = ['region']
    search_fields = ['name__startwith']
    ordering = ("name",)

admin.site.register(District, DistrictAdmin)

#Village
class VillageInline(admin.StackedInline):
    model = Village
    extra = 0

#wards
class WardAdmin(admin.ModelAdmin):
    list_display = ['view_id', 'name', 'district']
    list_filter = ['district']
    search_fields = ['name__startwith']
    ordering      = ("view_id",)
    inlines       = [VillageInline]

admin.site.register(Ward, WardAdmin)

#neighborhood
class NeighborhoodInline(admin.StackedInline):
    model = Neighborhood
    extra = 0

#villages
class VillageAdmin(admin.ModelAdmin):
    list_display  = ['view_id', 'name', 'ward']
    list_filter = ['ward']
    search_fields = ['name__startwith']
    ordering      = ("ward","view_id",)
    inlines       = [NeighborhoodInline]

admin.site.register(Village, VillageAdmin)