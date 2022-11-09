import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.citizen.models import Citizen
from apps.menu.models import *
from .utils import *

@csrf_exempt
def webhook(request):
    webhook_secret = "MA9447RTQAZAT6MWZXX393D9KCU3HEUR"
    message = "Welcome to Bukoba Project."

    if request.POST.get('secret') != webhook_secret:
        return HttpResponse("Invalid webhook secret", 'text/plain', 403)

    if request.POST.get('event') == 'incoming_message':
        key = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')

        print("key => " + key)
        print("from number => " + from_number)

        # check if phone number exist in database
        citizen = Citizen.objects.filter(phone=from_number)

        if citizen.count() == 0:
            if key.upper() == 'JIHAKIKI':
                #init first menu
                message = init_menu('TELERIVET', from_number)
            else:        
                #check menu session if active=0
                menu_session = MenuSession.objects.filter(phone=from_number, active=0)

                print("sessions => " + str(menu_session.count()))

                if menu_session.count() > 0:
                    # get latest menu session
                    m_session = MenuSession.objects.filter(phone=from_number, active=0).latest('id')

                    #check menu link
                    menu_response = check_menu_link(m_session.menu_id, key)

                    if menu_response == 'NEXT_MENU':
                        #update menu session data
                        m_session.active = 1
                        m_session.values = key
                        m_session.save()
                    
                        #call next menu
                        message = next_menu('TELERIVET', from_number, m_session.code, m_session.menu_id, key)

                    elif menu_response == 'INVALID_INPUT':
                        #message for invalid input
                        result = {'status': 'success', 'message': "Invalid input"}
                    elif menu_response == 'END_MENU':
                        #update menu active = 1
                        m_session.active = 1
                        m_session.save()

                        #init menu
                        message = init_menu('TELERIVET', from_number)   
                else:  
                    #init first menu
                    message = init_menu('TELERIVET', from_number)
        else:
            #return message 
            message = "Phone number already registered" 



        #return response to telerivet 
        return HttpResponse(json.dumps({
            'messages': [
                {'content': message}
            ]
        }), 'application/json')

