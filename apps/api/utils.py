import random
import string
import json
import requests
from django.http import JsonResponse
from apps.menu.models import *
from apps.location.models import *

#init menu
def init_menu(channel, phone):
    # get first menu
    menu = Menu.objects.get(flag="Jihakiki_Jina")

    #generate random key
    random_code = ''.join(random.choices(string.ascii_uppercase, k=12))

    # create menu session
    session = MenuSession()
    session.channel = channel    
    session.code = random_code
    session.menu_id = menu.id
    session.phone = phone
    session.save()

    # process menu
    message = process_menu(menu_id=menu.id, phone=phone)

    # response
    return message

#provess menu
def process_menu(menu_id, phone):
    # variables
    message = ""

    # get menu
    menu = Menu.objects.get(pk=menu_id)
    message = menu.title

    #modify menu to call ID Number
    if(menu.flag == 'Jihakiki_Verify_ID'):
        menu_session = MenuSession.objects.filter(menu_id=5, phone=phone).last()

        if menu_session:
            message = message.replace("ID_Number", menu_session.values)

    #if menu require to pull data
    if menu.pull == 1:
        response = requests.get(menu.pull_url)

        sub_message = ""
        for data in response.json()['response']:
            sub_message += data

        message = message + "\r\n" + sub_message  

    elif menu.pull == 0:     
        # get sub menu
        sub_menus = SubMenu.objects.filter(menu_id=menu_id).order_by('view_id')

        if(sub_menus):
            sub_message = ""
            for val in sub_menus:
                sub_message += val.view_id + ". " + val.title + "\r\n"

            message = message + "\r\n" + sub_message

    #message
    return message    

#check if there menu links
def check_menu_link(menu_id, key):
    sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id= key)

    if (sub_menu_key):
        menu_link = MenuLink.objects.filter(
            menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

        if(menu_link):
            return 'NEXT_MENU'
        else:
            return 'INVALID_INPUT'
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            return 'NEXT_MENU'
        else:
            return 'END_MENU'

#next menu
def next_menu(channel, phone, uuid, menu_id, key):
    # sub menu
    sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, view_id=key)

    message = ""
    if (sub_menu_key):
        # get menu link
        menu_link = MenuLink.objects.filter(
            menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

        if(menu_link):
            # create menu session
            session = MenuSession()
            session.channel = channel
            session.code = uuid
            session.menu_id = menu_link[0].link_id
            session.phone = phone
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id, phone)            
        else:
            # message
            message = "Invalid input"
    else:
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):
            # create menu session
            session = MenuSession()
            session.channel = channel
            session.code = uuid
            session.menu_id = menu_link[0].link_id
            session.phone = phone    
            session.save()

            # process menu
            message = process_menu(menu_link[0].link_id, phone)
        else:
            # message
            message = "Invalid input"

    return message


# process data
def process_data(uuid):
    menu_sessions = MenuSession.objects.filter(code=uuid)

    if(menu_sessions):
        arr_data = {}
        for menu_session in menu_sessions:
            menu = Menu.objects.get(pk=menu_session.menu_id)
            sub_menu = SubMenu.objects.filter(menu_id=menu.id)

            menu_value = ''
            if(sub_menu):
                sub_menu_value = SubMenu.objects.filter(menu_id=menu.id, view_id=menu_session.values)

                if(sub_menu_value):
                    menu_value = sub_menu_value[0].title

            else:
                menu_value = menu_session.values

            # assign all data to array
            if menu.label is not None and menu_value is not None:
                arr_data[menu.label] = menu_value

        #decide contact based on channel
        contact = menu_sessions[0].phone

        #response
        response = {
            'contents': arr_data, 
            'channel': menu_sessions[0].channel.upper(), 
            'contact': contact
        }
        return response
    else:
        return []


 #sending data
def save_data_session(uuid):
    #process data
    payload = process_data(uuid)

    #processed data
    print(json.dumps(payload))
        
    #browser response
    return JsonResponse({'status': 'success', 'message': "data saved"})


#select all wards
def get_wards(request):
    wards = Ward.objects.all()

    arr_wards = []
    for ward in wards:
        message = str(ward.id) + ". " + ward.name + "\r\n"
        arr_wards.append(message)

    return JsonResponse({"error": False, "response": arr_wards})


#select all wards
def get_villages(request):
    villages = Village.objects.all()

    arr_villages = []
    for village in villages:
        message = str(village.id) + ". " + village.name + "\r\n"
        arr_villages.append(message)

    return JsonResponse({"error": False, "response": arr_villages})