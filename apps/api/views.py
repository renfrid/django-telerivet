import json
from datetime import datetime
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
            if key.upper() == 'MTENDAJI' or key.upper() == 'MWENYEKITI' or key.upper() == 'MJUMBE' or key.upper() == 'MWANANCHI':
                message = telerivet.call_registration_menu(phone=from_number, key=key)
            else:        
                message ="Tuma neno  MTENDAJI au MWENYEKITI au MJUMBE au MWANANCHI kujisajili kwenye huduma hii sasa!"
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
            elif key.upper() == 'MWENYEKITI':
                if citizen.designation == 'MWENYEKITI':
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
            elif key.upper() == 'JEMBE':
                if citizen.designation == 'MWANANCHI':
                    if citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        message = 'Hii huduma itakujia hivi karibuni.'
                    else:
                        message = 'Umeshajisajili katika mfumo huu. Tafadhali wasiliana na mjumbe wako wa shina au afisa mtendaji wako wa mtaa kwa uhakiki ili uweze kutumia huduma ya JEMBE.'    
                else:
                    message = 'Huduma hii inatumiwa na mwananchi pekee.'    
            else:
                """split content into piece"""
                arr_key = key.split(' ', maxsplit=2)
                keyword = arr_key[0]

                if keyword.upper() == 'HAKIKI':
                    if citizen.status == 'COMPLETED':
                        message = 'Hauwezi kutumia huduma hii mpaka uwe umethibitishwa na ngazi ya juu. Tafadhali wasiliana na ngazi ya juu kwa uhakiki.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                        message = 'Samahani, akaunti yako imesitishwa. Tafadhali wasiliana na ngazi ya juu kurudisha akaunti yako.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        if arr_key[1] is None or arr_key[2] is None:
                            message = 'Umekosea kutumia huduma ya HAKIKI, kutumia huduma hii andika neno HAKIKA ikifuatiwa na Namba ya usajili na neno siri lako. Mfano HAKIKI MJB-999-45166 1234'  
                        else:
                            unique_id = arr_key[1] 
                            pin       = arr_key[2] 
                            """process HAKIKI thread"""
                            message = process_hakiki_thread(from_number=from_number, pin=pin, unique_id=unique_id, designation=citizen.designation)
                elif keyword.upper() == 'THIBITISHA': 
                    if citizen.status == 'COMPLETED':
                        message = 'Hauwezi kutumia huduma hii mpaka uwe umethibitishwa na ngazi ya juu. Tafadhali wasiliana na ngazi ya juu kwa uhakiki.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 0:
                        message = 'Samahani, akaunti yako imesitishwa. Tafadhali wasiliana na ngazi ya juu kurudisha akaunti yako.'
                    elif citizen.status == 'VERIFIED' and citizen.is_active == 1:
                        if arr_key[1] is None or arr_key[2] is None:
                            message = 'Umekosea kutumia huduma ya THIBITISHA, kutumia huduma hii andika neno THIBITISHA ikifuatiwa na Namba ya usajili na msimbo uliotumiwa wakati wa HAKIKI. Mfano THIBITISHA MJB-999-45166 1234'  
                        else:
                            unique_id = arr_key[1] 
                            otp       = arr_key[2] 
                            """process THIBITISHA thread"""
                            message = ""
                            message = process_thibitisha_thread(from_number=from_number, otp=otp, unique_id=unique_id, designation=citizen.designation)
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
                    print(my_data)
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
    """create profile for MTENDAJI, MWENYEKITI, MWANANCHI, MJUMBE"""
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
            citizen.ward_id            = response['arr_data']['working_ward']
            citizen.village_id         = response['arr_data']['working_village']

        elif citizen.designation == 'MWENYEKITI':
            citizen.ward_id            = response['arr_data']['working_ward']
            citizen.village_id         = response['arr_data']['working_village']
            citizen.hamlet             = response['arr_data']['hamlet']
            citizen.work               = response['arr_data']['work']
            citizen.physical_address   = response['arr_data']['house_number']

        elif citizen.designation == 'MJUMBE':
            citizen.ward_id            = response['arr_data']['working_ward']
            citizen.village_id         = response['arr_data']['working_village']
            citizen.shina              = response['arr_data']['working_shina']
            citizen.hamlet             = response['arr_data']['hamlet']

        elif citizen.designation == 'MWANANCHI':
            citizen.ward_id    = response['arr_data']['ward']
            citizen.village_id = response['arr_data']['village']
            citizen.hamlet     = response['arr_data']['hamlet']
            citizen.work       = response['arr_data']['work']
            citizen.physical_address = response['arr_data']['house_number']
            citizen.be_jembe = formating.format_be_jembe(be_jembe=response['arr_data']['be_jembe'])

        citizen.status = 'COMPLETED'
        citizen.save()

        """create customized message for user"""
        message = "Usajili wako wa awali umekamilika.Nambari yako ya usajili ni " + unique_id + ".\n\n"

        if citizen.designation == 'MTENDAJI':
            message += "Tafadhali wasiliana na afisa mtendaji wako wa kata kwa uhakiki."
        elif citizen.designation == 'MWENYEKITI':
            message += "Tafadhali wasiliana na afisa mtendaji wako wa kata kwa uhakiki."
        elif citizen.designation == 'MJUMBE':
            message += "Tafadhali wasiliana na afisa mtendaji wako wa kijiji au kata kwa uhakiki."
        elif citizen.designation == 'MWANANCHI': 
            message += "Tafadhali wasiliana na mjumbe au mtendaji wa kijiji kwa uhakiki."  

        """send unique number to the user"""
        telerivet.send_message(sender=phone, message=message)

        """send message to MTENDAJI_KATA"""
        if citizen.designation == 'MTENDAJI' or citizen.designation == 'MWENYEKITI':
            """send message to MTENDAJI_KATA"""

            """query for WEO"""
            qry_weo = Citizen.objects.filter(ward_id=citizen.ward_id, is_active=1, designation="MTENDAJI_KATA")

            if qry_weo.count() > 0:
                """WEO information"""
                qry_weo = qry_weo.last()
                qry_weo_phone = qry_weo.phone

                """message to WEO"""
                if citizen.designation == "MTENDAJI":
                    message_to_weo = "Habari, Mtendaji amejisajili.\n"
                elif citizen.designation == "MWENYEKITI":
                    message_to_weo = "Habari, Mwenyekiti amejisajili.\n" 

                """Add more message text"""     
                message_to_weo += "Namba: "+citizen.unique_id+"\n" \
                                "Jina: "+citizen.name+"\n" \
                                    "Kata: "+citizen.ward.name+"\n" \
                                        "Mtaa/Kijiji: "+citizen.village.name+"\n" \
                                        "Simu: "+citizen.phone

                """send message to WEO"""
                telerivet.send_message(sender=qry_weo_phone, message=message_to_weo)      

        elif citizen.designation == 'MJUMBE':
            """send message to MTENDAJI if was MJUMBE"""
            
            """query for MTENDAJI"""
            qry_veo = Citizen.objects.filter(village_id=citizen.village_id, is_active=1, designation="MTENDAJI")

            if qry_veo.count() > 0:
                """VEO data"""
                qry_veo = qry_veo.last()
                qry_veo_phone = qry_veo.phone

                """message to VEO"""
                message_to_veo = "Habari, mjumbe amejisajili.\n" \
                            "Namba: "+citizen.unique_id+"\n" \
                                "Jina: "+citizen.name+"\n" \
                                    "Kata: "+citizen.ward.name+"\n" \
                                        "Mtaa/Kijiji: "+citizen.village.name+"\n" \
                                                "Simu: "+citizen.phone

                """send message to VEO"""
                telerivet.send_message(sender=qry_veo_phone, message=message_to_veo)

        return HttpResponse({"error": False, 'success_msg': "data inserted and processed"})


def process_hakiki_thread(**kwargs):
    """process HAKIKI thread """ 
    from_number = kwargs['from_number']
    pin         = kwargs['pin']
    unique_id   = kwargs['unique_id']
    designation = kwargs['designation']

    """registration wrapper"""
    registration = RegistrationWrapper()

    citizen = Citizen.objects.filter(phone__exact=from_number, password__exact=pin)

    message = ""
    if citizen.count() > 0:
        citizen = citizen.first()

        """Check who uses the service"""
        if designation == "MWANANCHI":
            message = "Hauwezi kutumia huduma hii"
        else:
            qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id, ward_id=citizen.ward_id)    

            if qry_citizen.count() > 0:
                qry_citizen = qry_citizen.first()

                if qry_citizen.status == 'COMPLETED':
                    """generate OTP"""
                    otp = registration.generate_pin(pin_size=6)

                    """create or update OTP"""
                    obj, created = Token.objects.update_or_create(
                        verifier_id=citizen.id, client_id=qry_citizen.id,
                        defaults={'otp': otp, 'status': 1},
                    )

                    occupation = "Hakuna"
                    if qry_citizen.work is not None:
                        occupation = qry_citizen.work

                    hamlet = "Hakuna"
                    if qry_citizen.hamlet is not None:
                        hamlet = qry_citizen.hamlet 

                    """message"""
                    message = "Hakiki taarifa zifuatazo:\n" \
                        "Namba: "+ str(qry_citizen.unique_id) +"\n" \
                            "Jina: "+ qry_citizen.name +"\n" \
                                "Simu: " +qry_citizen.phone +"\n" \
                                    "Kazi: " + occupation + "\n" \
                                        "Kitambulisho: " + qry_citizen.id_type+"\n" \
                                            "Kitamb. Namba: "+ qry_citizen.id_number+"\n"\
                                                "Kata: " + qry_citizen.ward.name+"\n" \
                                                    "Mtaa/Kijiji: "+ qry_citizen.village.name+"\n" \
                                                        "Kitongoji: " + hamlet + "\n"\
                        "Kuthibitisha tuma neno THIBITISHA likifuatiwa na namba ya usajili, ikifuatiwa na namba ya msimbo huu wa siri "+ str(otp)+"\n" \
                        "Mfano: THIBITISHA MNC-999-54865 748593."
                elif qry_citizen.status == 'VERIFIED' and qry_citizen.is_active == 1:
                    message = "Samahani, namba ya usajili ya imeshahakikiwa."
            else:
                message = "Samahani, taarifa zako hazijakimilika"
    else:
        message = "Samahani, namba ya siri uliyoingiza sio sahihi. Hakikisha umeingiza tarakimu 4 tu." 

    """return  message"""
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

        """query verified citizen """
        qry_citizen = Citizen.objects.filter(unique_id__exact=unique_id, ward_id=citizen.ward.id) 

        if qry_citizen.count() > 0:
            qry_citizen = qry_citizen.first()

            if qry_citizen.designation == 'MTENDAJI':
                if designation == "MTENDAJI_KATA":
                    """query otp"""
                    qry_otp = Token.objects.filter(verifier_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1)

                    if qry_otp.count() > 0:
                        qry_otp = qry_otp.first()

                        """update otp to invalid"""
                        qry_otp.status = 0
                        qry_otp.save()

                        """update citizen to VERIFIED and ACTIVE=1"""
                        qry_citizen.status = 'VERIFIED'
                        qry_citizen.is_active = 1
                        qry_citizen.verified_at = datetime.now()
                        qry_citizen.verified_by_id = citizen.id
                        qry_citizen.save()

                        """TODO: create user profile for login to the platform"""

                        """Inform citizen after verification"""
                        message_to_citizen = "Habari, usajili wako umekamilika. Msimbo wako ni " + qry_citizen.password +"."
                        qry_citizen_phone = qry_citizen.phone
                        telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                        """message"""
                        message = "Ahsante, uhakiki wa taarifa za mtendaji mwenye namba ya usajili "+qry_citizen.unique_id+ "umekamilika."         
                    else:
                        message = "Samahani, umekosea msimbo au msimbo wako umeshatumika."
                else:
                    message = "Samahani, hauna uwezo kumuhakiki mtendaji wa kijiji."
            elif qry_citizen.designation == 'MWENYEKITI':
                if designation == "MTENDAJI_KATA":
                    """query otp"""
                    qry_otp = Token.objects.filter(verifier_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1)

                    if qry_otp.count() > 0:
                        qry_otp = qry_otp.first()

                        """update otp to invalid"""
                        qry_otp.status = 0
                        qry_otp.save()

                        """update citizen to VERIFIED and ACTIVE=1"""
                        qry_citizen.status = 'VERIFIED'
                        qry_citizen.is_active = 1
                        qry_citizen.verified_at = datetime.now()
                        qry_citizen.verified_by_id = citizen.id
                        qry_citizen.save()

                        """TODO: create user profile for login to the platform"""

                        """Inform citizen after verification"""
                        message_to_citizen = "Habari, usajili wako umekamilika. Msimbo wako ni " + qry_citizen.password +"."
                        qry_citizen_phone = qry_citizen.phone
                        telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                        """message"""
                        message = "Ahsante, uhakiki wa taarifa za mwenyekiti mwenye namba ya usajili "+qry_citizen.unique_id+ "umekamilika."         
                    else:
                        message = "Samahani, umekosea msimbo au msimbo wako umeshatumika."
                else:
                    message = "Samahani, hauna uwezo kumuhakiki mwenyekiti wa kijiji."
            elif qry_citizen.designation == 'MJUMBE':
                if designation == "MTENDAJI" or designation == "MWENYEKITI":
                    """query otp"""
                    qry_otp = Token.objects.filter(verifier_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1)

                    if qry_otp.count() > 0:
                        qry_otp = qry_otp.first()

                        """update otp to invalid"""
                        qry_otp.status = 0
                        qry_otp.save()

                        """update citizen to VERIFIED and ACTIVE=1"""
                        qry_citizen.status = 'VERIFIED'
                        qry_citizen.is_active = 1
                        qry_citizen.verified_at = datetime.now()
                        qry_citizen.verified_by_id = citizen.id
                        qry_citizen.save()

                        """TODO: create user profile for login to the platform"""

                        """Inform citizen after verification"""
                        message_to_citizen = "Habari, usajili wako umekamilika. Msimbo wako ni " + qry_citizen.password +"."
                        qry_citizen_phone = qry_citizen.phone
                        telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                        """message"""
                        message = "Ahsante, uhakiki wa taarifa za mjumbe mwenye namba ya usajili "+qry_citizen.unique_id+ "umekamilika."         
                    else:
                        message = "Samahani, umekosea msimbo au msimbo wako umeshatumika."
                else:
                    message = "Samahani, hauna uwezo kumuhakiki mjumbe wa kijiji."
            elif qry_citizen.designation == 'MWANANCHI':
                if designation == "MTENDAJI" or designation == "MWENYEKITI" or designation == "MJUMBE":
                    if designation == 'MJUMBE':
                        """query otp"""
                        qry_otp = Token.objects.filter(verifier_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1)

                        if qry_otp.count() > 0:
                            qry_otp = qry_otp.first() 

                            """update otp to invalid"""
                            qry_otp.status = 0
                            qry_otp.save()

                            """update citizen to PARTIAL and ACTIVE=0"""
                            qry_citizen.status = 'PARTIAL'
                            qry_citizen.is_active = 0
                            qry_citizen.verified_at = datetime.now()
                            qry_citizen.verified_by_id = citizen.id
                            qry_citizen.save()

                            """query for MTENDAJI"""
                            qry_veo = Citizen.objects.filter(village_id=citizen.village_id, is_active=1, designation="MTENDAJI")

                            if qry_veo.count() > 0:
                                """VEO data"""
                                qry_veo = qry_veo.last()
                                qry_veo_phone = qry_veo.phone
                                qry_veo_name = qry_veo.name

                                """message to VEO"""
                                message_to_veo = "Habari "+ qry_veo_name+", mjumbe wako "+ citizen.name + " " \
                                            "amekamilisha utambulisho wa awali wa mwananchi" \
                                                "mwenye namba za usajili "+ qry_citizen.unique_id 

                                """send message to VEO"""
                                telerivet.send_message(sender=qry_veo_phone, message=message_to_veo)

                            """query for Mwenyekiti"""
                            qry_mwenyekiti = Citizen.objects.filter(village_id=citizen.village_id, is_active=1, designation="MWENYEKITI")

                            if qry_mwenyekiti.count() > 0:
                                """MWENYEKITI data"""
                                qry_mwenyekiti = qry_mwenyekiti.last()
                                qry_mwenyekiti_phone = qry_mwenyekiti.phone
                                qry_mwenyekiti_name = qry_mwenyekiti.name

                                """message to MWENYEKITI"""
                                message_to_mwenyekiti = "Habari "+ qry_mwenyekiti_name+", mjumbe wako "+ citizen.name + " " \
                                            "amekamilisha utambulisho wa awali wa mwananchi" \
                                                "mwenye namba za usajili "+ qry_citizen.unique_id 

                                """send message to MWENYEKITI"""
                                telerivet.send_message(sender=qry_mwenyekiti_phone, message=message_to_mwenyekiti)

                            """Message to MWANANCHI"""
                            message_to_citizen = "Habari "+ qry_citizen.name+", uhakiki wa awali wa taarifa zako umekamilika. " \
                                            "Tafadhali wasiliana na ofisi ya afisa mtendaji wako kukamilisha usajili."

                            qry_citizen_phone = qry_citizen.phone

                            """send message to MWANANCHI"""
                            telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                            """message to MJUMBE after PARTIAL verification"""
                            message = "Ahsante "+ citizen.name +", uhakiki wa awali wa taarifa za mwananchi mwenye namba ya usajili "+ qry_citizen.unique_id+" umekamilika."        
                        else:
                            message = "Samahani, umekosea msimbo au msimbo wako umeshatumika."
                    elif designation == 'MTENDAJI' or designation == "MWENYEKITI":
                        """query otp"""
                        qry_otp = Token.objects.filter(verifier_id=citizen.id, client_id=qry_citizen.id, otp__exact=otp, status=1)

                        if qry_otp.count() > 0:
                            qry_otp = qry_otp.first()

                            """update otp to invalid"""
                            qry_otp.status = 0
                            qry_otp.save()

                            """update citizen to VERIFIED and ACTIVE=1"""
                            qry_citizen.status = 'VERIFIED'
                            qry_citizen.is_active = 1
                            qry_citizen.verified_at = datetime.now()
                            qry_citizen.verified_by_id = citizen.id
                            qry_citizen.save()

                            """TODO: create user profile for login to the platform"""

                            """query for Mwenyekiti"""
                            qry_mwenyekiti = Citizen.objects.filter(village_id=citizen.village_id, is_active=1, designation="MWENYEKITI")

                            if qry_mwenyekiti.count() > 0:
                                """MWENYEKITI data"""
                                qry_mwenyekiti = qry_mwenyekiti.last()
                                qry_mwenyekiti_phone = qry_mwenyekiti.phone
                                qry_mwenyekiti_name = qry_mwenyekiti.name

                                """message to MWENYEKITI"""
                                message_to_mwenyekiti = "Habari "+ qry_mwenyekiti_name+", " \
                                            "usajili wa mwananchi mwenye namba ya utambulisho "+ qry_citizen.unique_id +" umekamilika."

                                """send message to MWENYEKITI"""
                                telerivet.send_message(sender=qry_mwenyekiti_phone, message=message_to_mwenyekiti)

                            """Message to MJUMBE"""
                            qry_mjumbe = Citizen.objects.filter(village_id=citizen.village_id, is_active=1, designation="MJUMBE")

                            if qry_mwenyekiti.count() > 0:
                                """MJUMBE data"""
                                qry_mjumbe = qry_mjumbe.last()
                                qry_mjumbe_phone = qry_mjumbe.phone
                                qry_mjumbe_name = qry_mjumbe.name

                                """message to MJUMBE"""
                                message_to_mjumbe = "Habari "+ qry_mjumbe_name+", " \
                                            "usajili wa mwananchi mwenye namba ya utambulisho "+ qry_citizen.unique_id +" umekamilika."

                                """send message to MJUMBE"""
                                telerivet.send_message(sender=qry_mjumbe_phone, message=message_to_mjumbe)


                            """Message to MWANANCHI"""
                            message_to_citizen = "Habari " + qry_citizen.name + ", usajili wako umekamilika. " \
                                    "Neno siri ni " + qry_citizen.password + "."
                            qry_citizen_phone = qry_citizen.phone

                            """send message to MWANANCHI"""
                            telerivet.send_message(sender=qry_citizen_phone, message=message_to_citizen)

                            """message to MTENDAJI"""
                            message = "Ahsante "+ citizen.name + ", usajili wa mwananchi mwenye namba ya utambulisho "+ qry_citizen.unique_id +" umekamilika."         
                        else:
                            message = "Samahani, umekosea msimbo au msimbo wako umeshatumika."
                else:
                    message = "Samahani, hauna uwezo kumuhakiki mjumbe wa kijiji."
        else:
            message = "Samahani, taarifa zako hazijakimilika" 
    else:
        message = "Samahani, namba ya siri uliyoingiza sio sahihi. Hakikisha umeingiza tarakimu 4 tu." 

    """return message"""   
    return message   





            



        

        


