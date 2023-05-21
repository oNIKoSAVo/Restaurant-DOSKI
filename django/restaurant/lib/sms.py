import requests


# LOGIN = ""
# PASSWD = "49bd8d38-c4df-4e95-ad92-1761876849b7"
# API = "https://mcommunicator.ru/M2M/m2m_api.asmx/SendMessage"

class Sms:
    def send(self, number, password):
        # requests.packages.urllib3.disable_warnings()
        # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        # try:
        #     requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        # except AttributeError:
        #     # no pyopenssl support used / needed / available
        #     pass
        # response = requests.get(f"{API}?msid={phone}&message={message}&naming=beta.respublica.bar&login=&password={PASSWD}", verify=False)
        api_url = 'https://sms.ru/sms/send'
        api_key = 'B7D22505-86C0-C775-B786-968BE890FDA5'  # замените на свой API ключ
        sms_text = f'Ваш пароль: {password}'

        payload = {
            'api_id': api_key,
            'to': number,
            'msg': sms_text,
            'json': 1,
        }

        requests.post(api_url, data=payload)
        