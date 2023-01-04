from django.shortcuts import render
from .models import District, Neighborhood, Ward, Village

# Create your views here.


# Create your views here.
def get_districts(request, *args, **kwargs):
    if request.method == 'GET':
        region_id = kwargs['region_id']
        districts = District.objects.filter(region_id=region_id)

        # return response.
        return render(None, 'districts.html', {'districts': districts})

def get_wards(request, *args, **kwargs):
    if request.method == 'GET':
        district_id = kwargs['district_id']
        wards = Ward.objects.filter(district_id=district_id)

        # return response.
        return render(None, 'wards.html', {'wards': wards})


def get_villages(request, *args, **kwargs):
    if request.method == 'GET':
        ward_id = kwargs['ward_id']
        villages = Village.objects.filter(ward_id=ward_id)

        # return response.
        return render(None, 'villages.html', {'villages': villages})


def get_neighborhood(request, *args, **kwargs):
    if request.method == 'GET':
        village_id = kwargs['village_id']
        neighborhood = Neighborhood.objects.filter(village_id=village_id)

        # return response.
        return render(None, 'neighborhood.html', {'neighborhood': neighborhood})
