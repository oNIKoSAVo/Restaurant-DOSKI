import requests


class Payment:

    def create_terminal(self, order):
        response = requests.post("https://api.invoice.su/api/v2/CreateTerminal",
                                 headers={
                                     "Authorization": "Basic Nzk1MjkwNTY3MDY6ZDVkOThiYzI0YWZjMmM1OTNkOGEzMjMzOGJhZmI3ZmY=",
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

    def create_payment(self, order, receipt):
        response = requests.post("https://api.invoice.su/api/v2/CreatePayment",
                                 headers={
                                     "Authorization": "Basic Nzk1MjkwNTY3MDY6ZDVkOThiYzI0YWZjMmM1OTNkOGEzMjMzOGJhZmI3ZmY=",
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
                                         "terminal_id": "9a73af7faff347bf8844c66d8333ae84",
                                         "payment_method": "card",
                                         "success_url": "https://example.com/success",
                                         "fail_url": "https://example.com/error"
                                     },
                                     "custom_parameters": {},
                                     "receipt": receipt,
                                     "trtype": 1
                                 })

        return response.json()
