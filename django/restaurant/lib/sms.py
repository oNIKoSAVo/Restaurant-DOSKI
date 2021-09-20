import requests

LOGIN = "ivanxo"
PASSWD = "test1test"
API = "https://smsc.ru"

class Sms:
    def send(self, phone, message):
        response = requests.get(f"{API}/sys/send.php?login={LOGIN}&psw={PASSWD}&phones={phone}&mes={message}")
        print(response.text())