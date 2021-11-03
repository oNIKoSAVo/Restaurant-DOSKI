import requests

class Payment:

    def create_terminal(self, order, key):
        response = requests.post("https://api.invoice.su/api/v2/CreateTerminal",
                                 headers={
                                     "Authorization": f"Basic {key}",
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "name": "Республика",
                                     "description": "Зааказ доставки",
                                     "type": "dynamical",
                                     "defaultPrice": order.price
                                 }
                                 )

        return response.json()

    def create_payment(self, order, receipt, key, terminal):
        response = requests.post("https://api.invoice.su/api/v2/CreatePayment",
                                 headers={
                                     "Authorization": f"Basic {key}",
                                     "Content-Type": "application/json"
                                 },
                                 json={
                                     "order": {
                                         "currency": "RUB",
                                         "amount": order.price,
                                         "description": "Тестовый платеж",
                                         "id": order.id
                                     },
                                     "settings": {
                                         "terminal_id": terminal,
                                         "payment_method": "card",
                                         "success_url": "https://example.com/success",
                                         "fail_url": "https://example.com/error"
                                     },
                                     "custom_parameters": {},
                                     "receipt": receipt,
                                     "trtype": 1
                                 })

        return response.json()
