import random
import string
import json
import requests
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from apps.menu.models import *
from apps.location.models import *
from apps.account.models import *
from django.contrib.auth.models import User
from apps.citizen.models import Citizen
from decouple import config

class RegistrationWrapper:
    def __init__(self) -> None:
        pass

    def format_date(self, **kwargs):
        """format the date"""
        date_in = kwargs['date_in']

        if '-' in date_in:
            return datetime.strptime(date_in, '%d-%m-%Y').date() 
        elif '/' in date_in:    
            return datetime.strptime(date_in, '%d/%m/%Y').date() 
        elif '.' in date_in:    
            return datetime.strptime(date_in, '%d.%m.%Y').date() 
        else:
            return datetime.strptime('04/01/1990', '%d/%m/%Y').date() 


    def format_id_type(self, **kwargs):
        """format id type"""
        id_type = kwargs['id_type']

        if id_type == 'NIDA':
            label = "NIDA" 
        elif id_type == 'Leseni ya udereva':
            label = 'DRIVER LICENCE'
        elif id_type == 'Passport':
            label = 'PASSPORT'            
        elif id_type == 'Kitambulisho cha mpiga kura':
            label = 'VOTE ID' 
        elif id_type == 'Sina Kitambulisho':
            label = "SINA" 
        else:
            label = "SINA"      

        return label

    def format_gender(self, **kwargs):
        """format gender"""
        gender = kwargs['sex']

        if gender == "Mme":
            return 'M'
        else:
            return 'F'

    def format_be_jembe(self, **kwargs):
        """format gender"""
        be_jembe = kwargs['be_jembe']

        if be_jembe == "Ndiyo":
            return 1
        elif be_jembe == 'Hapana':
            return 0

    def generate_unique_id(self, **kwargs):
        """generate unique ID"""
        designation = kwargs['designation']
        postcode = "999"
        randno = random.randint(10000, 99999) 

        if designation == 'MTENDAJI_KATA':
            label = "WEO" 
        elif designation == 'MTENDAJI':
            label = 'VEO'
        elif designation == 'MWENYEKITI':
            label = 'MKT'            
        elif designation == 'MJUMBE':
            label = 'MJB' 
        elif designation == 'MWANANCHI':
            label = "MNC"   

        """concatenate"""
        unique_id = label + "-" + postcode + "-" + str(randno)   

        return unique_id     


    def generate_pin(self, **kwargs):
        """Generate pin for users"""
        pin_size = kwargs['pin_size']

        return ''.join(random.choice(string.digits) for x in range(pin_size)) 

    def format_phone(self, **kwargs):
        """Format phone number"""
        phone = kwargs['phone']
        
        if phone.startswith('0'):
            return "+255" + phone[1:]
        elif len(phone) == 9:
            return "+255" + phone
        else:
            return phone
    