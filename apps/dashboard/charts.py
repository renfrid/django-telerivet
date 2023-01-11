import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from apps.location.models import Ward,Village
from apps.citizen.models import Citizen


class WardChartView(APIView):
    """Display chart per ward"""
    def get(self, request, format=None):
        """GET data"""
        status = request.GET.get('status')

        """query wards"""
        wards = Ward.objects.all()

        arr_data = []
        for val in wards:
            """male citizens"""
            male_citizen = Citizen.objects.filter(ward_id=val.id, gender='M')

            if status != '' and status is not None:
                male_citizen = male_citizen.filter(status__exact = request.GET.get('status'))

            male_citizen = male_citizen.count()    
        
            """female citizen"""
            female_citizen = Citizen.objects.filter(ward_id=val.id, gender='F')

            if status != '' and status is not None:
                female_citizen = female_citizen.filter(status__exact = request.GET.get('status'))

            female_citizen = female_citizen.count()    

            """summation"""
            total_citizen = male_citizen + female_citizen

            #create dict
            chart = {
                'name': val.name,
                'total': int(total_citizen),
                'male': int(male_citizen),
                'female': int(female_citizen),
            } 
            arr_data.append(chart)

        """response"""
        return Response({"error": False, "chart" : arr_data})


