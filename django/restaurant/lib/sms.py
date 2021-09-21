import requests

LOGIN = ""
PASSWD = "49bd8d38-c4df-4e95-ad92-1761876849b7"
API = "https://mcommunicator.ru/M2M/m2m_api.asmx/SendMessage"

class Sms:
    def send(self, phone, message):
        response = requests.get(f"{API}?msid={phone}&message={message}&naming=beta.respublica.bar&login=&password={PASSWD}")
        print(response.text())