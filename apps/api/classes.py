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
import telerivet


class TelerivetWrapper:
    BASE_URL   = "http://127.0.0.1:8000/"
    API_TOKEN  = "MA9447RTQAZAT6MWZXX393D9KCU3HEUR"
    API_KEY = 'c7fAkAuMy8a6aUZQWyNNyYXSutXuszcV'
    PROJECT_ID = 'PJ592866ba523f191f'

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.BASE_URL


    def call_init_menu(self, **kwargs):
        """ Init First Menu """

        """args"""
        phone  = kwargs['phone']
        key    = kwargs['key']

        """menu"""
        if key == 'JIHAKIKI':
            menu = Menu.objects.get(flag="Jihakiki_Jina")
        elif key == 'MTENDAJI':
            menu = Menu.objects.get(flag="Mtendaji_Name") 

        """random code"""
        random_code = ''.join(random.choices(string.ascii_uppercase, k=12))

        """Create menu session"""
        session = MenuSession()   
        session.code = random_code
        session.menu_id = menu.id
        session.phone = phone
        session.save()

        message = self.process_menu(menu_id=menu.id, phone=phone)

        return message

    def call_registration_menu(self, **kwargs):
        """Registration Menu"""
        phone = kwargs['phone']
        key   = kwargs['key']

        """random code"""
        random_code = ''.join(random.choices(string.ascii_uppercase, k=12))

        """menu"""
        if key.upper() == 'JIHAKIKI':
            menu = Menu.objects.get(flag="Jihakiki_Jina")
            designation = "MWANANCHI"
        elif key.upper() == 'MTENDAJI':
            menu = Menu.objects.get(flag="Mtendaji_Name")
            designation = "MTENDAJI"

        menu_id = 16
        if menu:
            menu_id = menu.id

        """Create new temporary data"""
        citizen = Citizen()
        citizen.phone = phone 
        citizen.designation = designation 
        citizen.save()

        """create new session"""
        session = MenuSession()   
        session.code = random_code
        session.menu_id = menu_id
        session.phone = phone
        session.save()

        """process menu"""
        message = self.process_menu(menu_id, phone)

        return message


    def check_menu_link(self, menu_id, key):
        """Check Menu Link"""
        validate = self.validate_pull(menu_id, key)

        if validate == 'VALID':
            sub_menu = SubMenu.objects.filter(menu_id=menu_id)

            if sub_menu.count() > 0:
                sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key).first()

                if (sub_menu_key):
                    menu_link = MenuLink.objects.filter(
                        menu_id=menu_id, sub_menu_id=sub_menu_key.id)

                    if(menu_link):
                        return 'NEXT_MENU'
                    else:
                        return 'INVALID_INPUT'
                else:
                    return 'INVALID_INPUT'       
            else:
                menu_link = MenuLink.objects.filter(menu_id=menu_id)

                if(menu_link):
                    return 'NEXT_MENU'
                else:
                    return 'END_MENU'
        else:
            return 'INVALID_INPUT'; 


    def validate_pull(self, menu_id, key):
        """Validate pull information"""
        menu = Menu.objects.filter(pk=menu_id).first()

        if(menu):
            if menu.pull == 1:
                if menu.url == 'wards/':
                    """validate wards"""
                    ward = Ward.objects.filter(pk=key)

                    if(ward.count() > 0):
                        return 'VALID'
                    else:
                        return 'INVALID' 

                if menu.url == 'villages/':
                    """validate village"""
                    village = Village.objects.filter(pk=key)

                    if(village.count() > 0):
                        return 'VALID'
                    else:
                        return 'INVALID'
            else:
                return 'VALID'                              
        else:
            return 'INVALID' 


    def next_menu(self, **kwargs):
        """Triggering Next Menu"""
        phone   = kwargs['phone']
        uuid    = kwargs['uuid']
        menu_id = kwargs['menu_id']
        key     = kwargs['key']

        """action"""
        action = None

        """sub menu"""
        sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key)

        message = ""
        if (sub_menu_key):
            menu_link = MenuLink.objects.filter(
                menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

            if(menu_link):
                """create menu session"""
                session = MenuSession()
                session.code = uuid
                session.menu_id = menu_link[0].link_id
                session.phone = phone
                session.save()

                """process menu"""
                message = self.process_menu(menu_link[0].link_id, phone)            
            else:
                """message"""
                message = "Invalid input"
        else:
            menu_link = MenuLink.objects.filter(menu_id=menu_id)

            if(menu_link):
                """create menu session"""
                session = MenuSession()
                session.code = uuid
                session.menu_id = menu_link[0].link_id
                session.phone = phone    
                session.save()

                """process menu"""
                message = self.process_menu(menu_link[0].link_id, phone)
                menu = Menu.objects.get(pk=menu_link[0].link_id)

                if menu.action is not None:
                    action = menu.action
            else:
                """message"""
                message = "Invalid input"

        return JsonResponse({'status': 'success', 'message': message, 'action': action})

    def process_menu(self, menu_id, phone):
        """Process Menu"""
        message = ""

        menu = Menu.objects.get(pk=menu_id)
        message = menu.title

        if menu.flag == 'Jihakiki_Verify_ID':
            menu_session = MenuSession.objects.filter(menu_id=5, phone=phone).last()

            if menu_session:
                message = message.replace("ID_Number", menu_session.values)

        if menu.flag == 'Mtendaji_Verify_ID':
            menu_session = MenuSession.objects.filter(menu_id=26, phone=phone).last()

            if menu_session:
                message = message.replace("ID_Number", menu_session.values)

        if menu.pull == 1:
            """Construct URL"""
            URL = self.BASE_URL + menu.url

            """response"""
            response = requests.get(URL)

            sub_message = ""
            for data in response.json()['response']:
                sub_message += data

            message = message + "\r\n" + sub_message  

        elif menu.pull == 0:     
            sub_menus = SubMenu.objects.filter(menu_id=menu_id).order_by('view_id')

            if(sub_menus):
                sub_message = ""
                for val in sub_menus:
                    sub_message += val.view_id + ". " + val.title + "\r\n"

                message = message + "\r\n" + sub_message
        return message 


    def send_message(self, **kwargs):
        """Send message to telerivet"""
        sender  = kwargs["sender"]
        message = kwargs["message"]

        tr = telerivet.API(self.API_KEY)
        project = tr.initProjectById(self.PROJECT_ID)

        sent_msg = project.sendMessage(
            to_number = sender,
            content = message
        )
        print(sent_msg)

        return HttpResponse({'error': False, 'success_msg': "Message sent!"})


    def process_data(self, **kwargs):
        """Process data for processing"""
        uuid  = kwargs["uuid"]

        """menu sessions"""
        menu_sessions = MenuSession.objects.filter(code=uuid)

        if menu_sessions:
            arr_data = {}
            for menu_session in menu_sessions:
                menu = Menu.objects.get(pk=menu_session.menu_id)
                sub_menu = SubMenu.objects.filter(menu_id=menu.id)

                menu_value = ''
                if sub_menu:
                    sub_menu_value = SubMenu.objects.filter(menu_id=menu.id, view_id=menu_session.values).first()

                    if sub_menu_value:
                        menu_value = sub_menu_value.title
                else:
                    menu_value = menu_session.values

                """assign all data to array"""
                if menu.label is not None and menu_value is not None:
                    arr_data[menu.label] = menu_value

            """response"""
            return JsonResponse({'status': 'success', 'arr_data': arr_data})
        else:
            return JsonResponse({'status': 'failed', 'error_msg': 'No any data!'})
            
