import requests

LOGIN = ""
PASSWD = "724f681c-734f-4810-b128-e11f07f3eb60"
API = "https://mcommunicator.ru/M2M/m2m_api.asmx/SendMessage"

class Sms:
    def send(self, phone, message):
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass
        response = requests.get(f"{API}?msid={phone}&message={message}&naming=BARDOSKI&login=&password={PASSWD}", verify=False)
