import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.citizen.models import Citizen
from apps.menu.models import *
from apps.location.models import *
from .classes import TelerivetWrapper
from .registration import RegistrationWrapper


@csrf_exempt
def webhook(request):
    """Webhook for receiving message from Telerivet"""
    webhook_secret = "MA9447RTQAZAT6MWZXX393D9KCU3HEUR"
    message = "Welcome to Bukoba Project."

    # telerivet = TelerivetWrapper()
    # telerivet.send_message(sender='+255717705746', message=message)

    # return HttpResponse('executed')

    if request.POST.get('secret') != webhook_secret:
        return HttpResponse("Invalid webhook secret", 'text/plain', 403)

    if request.POST.get('event') == 'incoming_message':
        key = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')

        print("key => " + key)
        print("from number => " + from_number)
        print("phone id => " + phone_id)

        """telerivet wrapper"""
        telerivet = TelerivetWrapper()

        """profile"""
        citizen = Citizen.objects.filter(phone=from_number)

        if citizen.count() == 0:
            if key.upper() == 'JIHAKIKI' or key.upper() == 'MTENDAJI' or key.upper() == 'MJUMBE':
                message = telerivet.call_registration_menu(phone=from_number, key=key)
            else:        
                message ="Tuma neno JIHAKIKI au MTENDAJI au MJUMBE kujisajili sasa"
        else:
            """Follow menu session and Trigger follow up menu"""
            menu_session = MenuSession.objects.filter(phone=from_number, active=0) 

            if menu_session.count() > 0:
                m_session = MenuSession.objects.filter(phone=from_number, active=0).latest('id')
                menu_response = telerivet.check_menu_link(m_session.menu_id, key) 

                if menu_response == 'NEXT_MENU':
                    """update menu session"""
                    m_session.active = 1
                    m_session.values = key
                    m_session.save()

                    """update data if involves JIHAKIKI menu"""
                    OD_uuid = m_session.code
                    OD_menu_id = m_session.menu_id

                    """result"""
                    result = telerivet.next_menu(phone=from_number, uuid=OD_uuid, menu_id=OD_menu_id, key=key)
                    data = json.loads(result.content)

                    """message"""
                    message = data['message']

                    """check for action = None"""
                    if(data['action'] is not None):
                        if data['action'] == 'create':
                            """update all menu session"""
                            m_session.active = 1
                            m_session.save()

                            """process data"""
                            response = telerivet.process_data(uuid=OD_uuid)
                            my_data = json.loads(response.content)
                            result = create_profile(phone=from_number, response=my_data)

                elif menu_response == 'INVALID_INPUT':
                    """invalid input"""
                    message = "Chagua batili, tafadhali chagua tena!"

                elif menu_response == 'END_MENU':
                    """update and end menu session"""
                    m_session.active = 1
                    m_session.save()

                    """initiate menu session"""
                    message = "Asante kwa kukamilisha usajili wako!"    
            else:
                """initiate menu session"""
                message = telerivet.call_init_menu(phone=from_number, key=key)     

        return HttpResponse(json.dumps({
            'messages': [
                {"content": message}
            ]
        }), 'application/json') 

    else:
        print("Failed message")
        return HttpResponse(json.dumps({
            "message": "Failed"
        })) 


 

def create_profile(**kwargs):
    """create profile for MTENDAJI, MWANANCHI, MJUMBE"""
    phone    = kwargs['phone']
    response = kwargs['response']

    """registration wrapper"""
    formating = RegistrationWrapper()

    """telerivet wrapper"""
    telerivet = TelerivetWrapper()

    """query for citizen"""
    citizen = Citizen.objects.filter(phone=phone).first()

    if citizen:
        """process data"""
        name      = response['arr_data']['name']
        gender    = formating.format_gender(sex=response['arr_data']['sex'])
        dob       = formating.format_date(date_in=response['arr_data']['dob'])
        id_type   = response['arr_data']['id_type']
        id_number = response['arr_data']['id_number']

        """process PIN"""
        password = formating.generate_pin(pin_size=6)

        """generate unique number"""
        unique_id = formating.generate_unique_id(designation=citizen.designation)

        """starting update data"""
        citizen.name      = name
        citizen.gender    = gender
        citizen.dob       = dob
        citizen.id_type   = id_type
        citizen.id_number = id_number
        citizen.password  = password
        citizen.unique_id = unique_id

        if citizen.designation == 'MTENDAJI':
            working_ward    = response['arr_data']['working_ward']
            working_village = response['arr_data']['working_village']

            citizen.working_ward_id    = working_ward
            citizen.working_village_id = working_village

        citizen.status = 'COMPLETED'
        citizen.save()

        """create customized message for user"""
        message = "Usajili wako wa awali umekamilika.Nambari yako ya usajili ni " + unique_id + ".\n\n"
        message += "Tafadhali wasiliana na afisa mtendaji wako wa kata kwa uhakiki."

        """send PIN to the user"""
        telerivet.send_message(sender=phone, message=message)

        """TODO: send message to weo"""
        """TODO: send message to VEO if was MJUMBE"""
        """TODO: send message to VEO and MJUMBE if was Mwananchi"""

        return HttpResponse({"error": False, 'success_msg': "data inserted and processed"})


            



        

        


