import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.citizen.models import Citizen, Token
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
        content = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')

        """split content into piece"""
        keyword = content.split(' ', maxsplit=2)
        key = keyword[0]

        print("key => " + key)
        print("from number => " + from_number)
        print("phone id => " + phone_id)

        """telerivet wrapper"""
        telerivet = TelerivetWrapper()

        """profile"""
        citizen = Citizen.objects.filter(phone=from_number)

        if citizen.count() == 0:
            if key.upper() == 'MTENDAJI' or key.upper() == 'MJUMBE' or key.upper() == 'MWANANCHI':
                message = telerivet.call_registration_menu(phone=from_number, key=key)
            else:        
                message ="Tuma neno  MTENDAJI au MJUMBE au MWANANCHI kujisajili kwenye huduma hii sasa!"
        else:
            """initialize citizen"""
            citizen = citizen.first()

            """todo: check other options for keyword"""
            if key.upper() == 'MTENDAJI':
                if citizen.designation == 'MTENDAJI':
                    if citizen.status == 'COMPLETED':
                        message = 'Umeshajisajili katika mfumo huu. Tafadhali wasiliana na afisa mtendaji wako wa kata kwa uhakiki.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        message = 'Habari, usajili wako umekamilika. Tuma neno HABARI kutuma taarifa kwa wananchi wa mtaa wako.'  
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                        message = 'Samahani, namba ya usajili ya mtendaji imeshahakikiwa au imesitishwa.'
                    elif citizen.status == 'PENDING':
                        message = process_threads(from_number=from_number, key=key, designation=citizen.designation)   
                else:
                    message = 'Namba imeshatumika kwa huduma nyingine'
            elif key.upper() == 'MJUMBE':
                if citizen.designation == 'MJUMBE':
                    if citizen.status == 'COMPLETED':
                        message = 'Umeshajisajili katika mfumo huu. Tafadhali wasiliana na afisa mtendaji wako wa mtaa kwa uhakiki.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        message = 'Habari, usajili wako umekamilika.'  
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                        message = 'Samahani, namba ya usajili ya mjumbe imeshahakikiwa au imesitishwa.'
                    elif citizen.status == 'PENDING':
                        message = process_threads(from_number=from_number, key=key, designation=citizen.designation)   
                else:
                    message = 'Namba imeshatumika kwa huduma nyingine'
            elif key.upper() == 'MWANANCHI':
                if citizen.designation == 'MWANANCHI':
                    if citizen.status == 'COMPLETED':
                        message = 'Umeshajisajili katika mfumo huu. Tafadhali wasiliana na mjumbe wako wa shina au afisa mtendaji wako wa mtaa kwa uhakiki.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        message = 'JEMBE ni huduma inayompa mwananchi mwenye simu ya mkononi uwezo wa kuwasajili wananchi wengine wasiokuwa na simu ya mkononi ndani ya mtaa/kijiji chake. JEMBE huchaguliwa na afisa mtendaji wa mtaa/kijiji wako/chako.\n\nKupiga JEMBE, tuma neno JEMBE kisha fuata maelekezo.'  
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                        message = 'Samahani, akaunti yako imesitishwa. Tafadhali wasiliana na mtendaji wa mtaa wako kurudisha akaunti yako.'
                    elif citizen.status == 'PENDING':
                        message = process_threads(from_number=from_number, key=key, designation=citizen.designation)   
                else:
                    message = 'Namba imeshatumika kwa huduma nyingine' 
            elif key.upper() == 'HAKIKI':
                if citizen.status == 'COMPLETED':
                    message = 'Hauwezi kutumia huduma hii mpaka uwe umethibitishwa na ngazi ya juu. Tafadhali wasiliana na ngazi ya juu kwa uhakiki.'
                elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                    message = 'Samahani, akaunti yako imesitishwa. Tafadhali wasiliana na ngazi ya juu kurudisha akaunti yako.'
                elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                    if keyword[1] is None or keyword[2] is None:
                        message = 'Umekosea kutumia huduma ya HAKIKI, kutumia huduma hii andika neno HAKIKA ikifuatiwa na Namba ya usajili na neno siri lako. Mfano HAKIKI MJB-999-45166 1234'  
                    else:
                        unique_id = keyword[1] 
                        pin       = keyword[2] 
                        """process HAKIKI thread"""
                        message = process_hakiki_thread(from_number=from_number, pin=pin, unique_id=unique_id, designation=citizen.designation)
            elif key.upper() == 'THIBITISHA':   
                if citizen.status == 'COMPLETED':
                    message = 'Hauwezi kutumia huduma hii mpaka uwe umethibitishwa na ngazi ya juu. Tafadhali wasiliana na ngazi ya juu kwa uhakiki.'
                elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                    message = 'Samahani, akaunti yako imesitishwa. Tafadhali wasiliana na ngazi ya juu kurudisha akaunti yako.'
                elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                    if keyword[1] is None or keyword[2] is None:
                        message = 'Umekosea kutumia huduma ya THIBITISHA, kutumia huduma hii andika neno THIBITISHA ikifuatiwa na Namba ya usajili na msimbo uliotumiwa wakati wa HAKIKI. Mfano THIBITISHA MJB-999-45166 1234'  
                    else:
                        unique_id = keyword[1] 
                        otp       = keyword[2] 
                        """process THIBITISHA thread"""
                        message = ""
                        message = process_thibitisha_thread(from_number=from_number, otp=otp, unique_id=unique_id, designation=citizen.designation)              
            elif key.upper() == 'JEMBE':
                if citizen.designation == 'MWANANCHI':
                    if citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        message = 'Hii huduma itakujia hivi karibuni.'
                    else:
                        message = 'Umeshajisajili katika mfumo huu. Tafadhali wasiliana na mjumbe wako wa shina au afisa mtendaji wako wa mtaa kwa uhakiki ili uweze kutumia huduma ya JEMBE.'    
                else:
                    message = 'Huduma hii inatumiwa na mwananchi pekee.'    
            else:
                message = process_threads(from_number=from_number, key=key, designation=citizen.designation)

        """return response to telerivet"""
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


def process_threads(**kwargs):
    """process all the threads"""
    from_number = kwargs['from_number']
    key         = kwargs['key']
    designation = kwargs['designation']

    """initiate message"""
    message = "Welcome to Bukoba Project."

    """telerivet wrapper"""
    telerivet = TelerivetWrapper()

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
            result = telerivet.next_menu(phone=from_number, uuid=OD_uuid, menu_id=OD_menu_id, key=key, designation=designation)
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
        message = telerivet.call_init_menu(phone=from_number, key=key, designation=designation) 

    return message    


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
        password = formating.generate_pin(pin_size=4)

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
            citizen.working_ward_id    = response['arr_data']['working_ward']
            citizen.working_village_id = response['arr_data']['working_village']

        elif citizen.designation == 'MJUMBE':
            citizen.working_ward_id    = response['arr_data']['working_ward']
            citizen.working_village_id = response['arr_data']['working_village']
            citizen.working_shina = response['arr_data']['working_shina']

        elif citizen.designation == 'MWANANCHI':
            citizen.ward_id    = response['arr_data']['ward']
            citizen.village_id = response['arr_data']['village']
            citizen.hamlet     = response['arr_data']['hamlet']
            citizen.work       = response['arr_data']['work']
            citizen.physical_address = response['arr_data']['house_number']
            citizen.be_jembe = response['arr_data']['be_jembe']

        citizen.status = 'COMPLETED'
        citizen.save()

        """create customized message for user"""
        message = "Usajili wako wa awali umekamilika.Nambari yako ya usajili ni " + unique_id + ".\n\n"
        message += "Tafadhali wasiliana na afisa mtendaji wako wa kata kwa uhakiki."

        """send unique number to the user"""
        telerivet.send_message(sender=phone, message=message)

        """send message to WEO"""
        if citizen.designation == 'MTENDAJI':
            """query for WEO"""
            weo = Citizen.objects.filter(ward_id=citizen.working_ward_id, is_active=1, designation="WEO")

            if weo.count() > 0:
                """WEO data"""
                weo = weo.last()
                weo_phone = weo.phone

                """message to WEO"""
                message_to_weo = "Habari, mtendaji amejisajili.\n" \
                            "Namba: "+citizen.unique_id+"\n" \
                                "Jina: "+citizen.name+"\n" \
                                    "Kata: "+citizen.working_ward.name+"\n" \
                                        "Mtaa/Kijiji: "+citizen.working_village.name+"\n" \
                                                "Simu: "+citizen.phone

                """send message to WEO"""
                telerivet.send_message(sender=weo_phone, message=message_to_weo)

        """send message to VEO if was MJUMBE"""
        if citizen.designation == 'MJUMBE':
            """query for VEO"""
            veo = Citizen.objects.filter(village_id=citizen.working_village_id, is_active=1, designation="MTENDAJI")

            if veo.count() > 0:
                """VEO data"""
                veo = veo.last()
                veo_phone = veo.phone

                """message to VEO"""
                message_to_veo = "Habari, mjumbe amejisajili.\n" \
                            "Namba: "+citizen.unique_id+"\n" \
                                "Jina: "+citizen.name+"\n" \
                                    "Kata: "+citizen.working_ward.name+"\n" \
                                        "Mtaa/Kijiji: "+citizen.working_village.name+"\n" \
                                                "Simu: "+citizen.phone

                """send message to WEO"""
                telerivet.send_message(sender=veo_phone, message=message_to_veo)


        """send message to VEO and MJUMBE if was Mwananchi"""
        if citizen.designation == 'MWANANCHI':
            """query for VEO"""
            veo = Citizen.objects.filter(village_id=citizen.working_village_id, is_active=1, designation="MTENDAJI")

            if veo.count() > 0:
                """VEO data"""
                veo = veo.last()
                veo_phone = veo.phone

                """message to VEO"""
                message_to_veo = "Habari, mjumbe amejisajili.\n" \
                            "Namba: "+citizen.unique_id+"\n" \
                                "Jina: "+citizen.name+"\n" \
                                    "Kata: "+citizen.working_ward.name+"\n" \
                                        "Mtaa/Kijiji: "+citizen.working_village.name+"\n" \
                                                "Simu: "+citizen.phone

                """send message to VEO"""
                telerivet.send_message(sender=veo_phone, message=message_to_veo)

        """query for VEO"""
        mjumbe = Citizen.objects.filter(village_id=citizen.working_village_id, is_active=1, designation="MJUMBE")

        if mjumbe.count() > 0:
            """MJUMBE data"""
            mjumbe = mjumbe.last()
            mjumbe_phone = mjumbe.phone

            """message to MJUMBE"""
            message_to_mjumbe = "Habari, mjumbe amejisajili.\n" \
                        "Namba: "+citizen.unique_id+"\n" \
                            "Jina: "+citizen.name+"\n" \
                                "Kata: "+citizen.working_ward.name+"\n" \
                                    "Mtaa/Kijiji: "+citizen.working_village.name+"\n" \
                                            "Simu: "+citizen.phone

            """send message to MJUMBE"""
            telerivet.send_message(sender=mjumbe_phone, message=message_to_mjumbe)

        return HttpResponse({"error": False, 'success_msg': "data inserted and processed"})

def process_hakiki_thread(**kwargs):
    """process HAKIKI thread """ 
    from_number = kwargs['from_number']
    pin         = kwargs['pin']
    unique_id   = kwargs['unique_id']
    designation = kwargs['designation']

    """registration wrapper"""
    formating = RegistrationWrapper()

    citizen = Citizen.objects.filter(phone__exact=from_number, password__exact=pin)

    message = ""
    if citizen.count() > 0:
        citizen = citizen.first()
        """query citizen belong based on WEO"""
        if designation == "WEO":
            qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id,ward_id=citizen.id)

            if qry_citizen.count() > 0:
                qry_citizen = qry_citizen.first()

                if qry_citizen.status == 'COMPLETE':
                    """generate OTP"""
                    otp = formating.generate_pin(pin_size=6)

                    """create or update OTP"""
                    obj, created = Token.objects.update_or_create(
                        citizen_id=citizen.id, client_id=qry_citizen.id,
                        defaults={'otp': otp, 'status': 1},
                    )

                    """message"""
                    message = "Hakiki taarifa zifuatazo:\n" \
                            "Namba: "+qry_citizen.unique_id+"\n" \
                            "Jina: "+qry_citizen.name+"\n" \
                            "Simu: "+qry_citizen.phone+"\n" \
                            "Kazi: "+qry_citizen.work+"\n" \
                            "Kitambulisho: "+qry_citizen.id_type+"\n" \
                            "Kitamb. Namba: "+ qry_citizen.id_number+"\n"\
                            "Kata: "+qry_citizen.ward.name+"\n" \
                            "Mtaa/Kijiji: "+qry_citizen.village.name+"\n" \
                            "Kitongoji: "+qry_citizen.hamlet+"\n"\
                            "Kuthibitisha tuma neno THIBITISHA likifuatiwa na namba ya usajili ya mwananchi, ikifuatiwa na namba ya msimbo huu wa siri "+otp+"\n" \
                            "Mfano: THIBITISHA MNC-999-54865 748593."
                elif qry_citizen.status == 'VERIFIED' and qry_citizen.is_active == 1:
                    message = "Samahani, namba ya usajili ya imeshahakikiwa."
            else:
                message = "Samahani, taarifa zako hazijakimilika"

        elif designation == 'MTENDAJI' or designation == 'MJUMBE':
            qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id,ward_id=citizen.ward.id, village_id=citizen.village.id)

            if qry_citizen.count() > 0:
                qry_citizen = qry_citizen.first()

                if qry_citizen.status == 'COMPLETE':
                    """generate OTP"""
                    otp = formating.generate_pin(pin_size=6)

                    """create or update OTP"""
                    obj, created = Token.objects.update_or_create(
                        citizen_id=citizen.id, client_id=qry_citizen.id,
                        defaults={'otp': otp, 'status': 1},
                    )

                    """message"""
                    message = "Hakiki taarifa zifuatazo:\n" \
                            "Namba: "+qry_citizen.unique_id+"\n" \
                            "Jina: "+qry_citizen.name+"\n" \
                            "Simu: "+qry_citizen.phone+"\n" \
                            "Kazi: "+qry_citizen.work+"\n" \
                            "Kitambulisho: "+qry_citizen.id_type+"\n" \
                            "Kitamb. Namba: "+ qry_citizen.id_number+"\n"\
                            "Kata: "+qry_citizen.ward.name+"\n" \
                            "Mtaa/Kijiji: "+qry_citizen.village.name+"\n" \
                            "Kitongoji: "+qry_citizen.hamlet+"\n"\
                            "Kuthibitisha tuma neno THIBITISHA likifuatiwa na namba ya usajili ya mwananchi, ikifuatiwa na namba ya msimbo huu wa siri "+otp+"\n" \
                            "Mfano: THIBITISHA MNC-999-54865 748593."
                elif qry_citizen.status == 'VERIFIED' and qry_citizen.is_active == 1:
                    message = "Samahani, namba ya usajili ya imeshahakikiwa."
            else:
                message = "Samahani, taarifa zako hazijakimilika"

        elif designation == 'MWANANCHI':
            message = "Hauwezi kutumia huduma hii"
    else:
        message = "Samahani, namba ya siri uliyoingiza sio sahihi. Hakikisha umeingiza tarakimu 4 tu."    

    return message


def process_thibitisha_thread(**kwargs):
    """process HAKIKI thread """ 
    from_number = kwargs['from_number']
    otp         = kwargs['otp']
    unique_id   = kwargs['unique_id']
    designation = kwargs['designation']

    """telerivet wrapper"""
    telerivet = TelerivetWrapper()

    citizen = Citizen.objects.filter(phone__exact=from_number)        

    message = ""
    if citizen.count() > 0:
        citizen = citizen.first()

        """query citizen belong based on WEO"""
        if designation == "WEO":
            qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id,ward_id=citizen.id)

            if qry_citizen.count() > 0:
                qry_citizen = qry_citizen.first()

                """query otp"""
                qry_otp = Token.objects.filter(citizen_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1).first()

                if qry_otp: 
                    """update otp to invalid"""
                    qry_otp.status = 0
                    qry_otp.save()

                    """update citizen to VERIFIED and ACTIVE=1"""
                    qry_citizen.status = 'VERIFIED'
                    qry_citizen.is_active = 1
                    qry_citizen.save()

                    """Inform citizen after verification"""
                    message_to_citizen = "Habari, usajili wako umekamilika. Tuma neno JIHAKIKI kupata huduma za JIHAKIKI."
                    qry_citizen_phone = qry_citizen.phone
                    telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                    """message"""
                    message = "Ahsante, uhakiki wa taarifa za mwananchi mwenye namba ya usajili "+qry_citizen.unique_id+ "umekamilika."
            else:
                message = "Samahani, taarifa zako hazijakimilika"  

        elif designation == 'MTENDAJI' or designation == 'MJUMBE': 
            qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id,ward_id=citizen.ward.id, village_id=citizen.village.id)

            if qry_citizen.count() > 0:
                qry_citizen = qry_citizen.first()

                """query otp"""
                qry_otp = Token.objects.filter(citizen_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1).first()

                if qry_otp: 
                    """update otp to invalid"""
                    qry_otp.status = 0
                    qry_otp.save()

                    """update citizen to VERIFIED and ACTIVE=1"""
                    qry_citizen.status = 'VERIFIED'
                    qry_citizen.is_active = 1
                    qry_citizen.save()

                    """Inform citizen after verification"""
                    message_to_citizen = "Habari, usajili wako umekamilika. Tuma neno JIHAKIKI kupata huduma za JIHAKIKI."
                    qry_citizen_phone = qry_citizen.phone
                    telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                    """message"""
                    message = "Ahsante, uhakiki wa taarifa za mwananchi mwenye namba ya usajili "+qry_citizen.unique_id+ "umekamilika."
            else:
                message = "Samahani, taarifa zako hazijakimilika" 

        elif designation == 'MWANANCHI':
            message = "Hauwezi kutumia huduma hii"  
    else:
        message = "Samahani, namba ya siri uliyoingiza sio sahihi. Hakikisha umeingiza tarakimu 4 tu." 

    """return message"""   
    return message   





            



        

        


