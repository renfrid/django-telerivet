import random
import string
import json
import requests
from django.http import JsonResponse
from apps.menu.models import *
from apps.location.models import *

def get_wards(request):
    """select all wards based on phone id"""
    wards = Ward.objects.all()

    arr_wards = []
    for ward in wards:
        message = str(ward.id) + ". " + ward.name + "\r\n"
        arr_wards.append(message)

    return JsonResponse({"error": False, "response": arr_wards})


def get_villages(request):
    """select all wards based on phone id and ward id"""

    """args"""
    messageId   = request.GET.get('message_id')
    designation = request.GET.get("designation")

    """menu session"""
    if designation == 'MTENDAJI':
        menu_session = MenuSession.objects.filter(code=messageId, flag='Mtendaji_Kata_Utumishi').first()
    elif designation == 'MWENYEKITI':
        menu_session = MenuSession.objects.filter(code=messageId, flag='Mwenyekiti_Kata_Utumishi').first()
    elif designation == 'MJUMBE':
        menu_session = MenuSession.objects.filter(code=messageId, flag='Mjumbe_Kata_Utumishi').first() 
    elif designation == 'MWANANCHI':   
        menu_session = MenuSession.objects.filter(code=messageId, flag='Mwananchi_Ward').first()

    if menu_session:
        ward_id = menu_session.values
        villages = Village.objects.filter(ward_id=ward_id)
    else:    
        villages = Village.objects.all()

    arr_villages = []
    for village in villages:
        message = str(village.id) + ". " + village.name + "\r\n"
        arr_villages.append(message)

    return JsonResponse({"error": False, "response": arr_villages})