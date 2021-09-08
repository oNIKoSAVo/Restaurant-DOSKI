import requests


class Payment:

    def create_terminal(self, order):
        response = requests.post("https://api.invoice.su/api/v2/CreateTerminal",
                                 headers={
                                     "Authorization": "Basic YzI0MzYwY2ZhYzBhMGM0MGM1MTg0MDVmNmJjNjhjYjA6MTUyNmZlYzAxYjVkMTFmNGRmNGYyMTYwNjI3Y2UzNTE=",
                                     "Content-Type": "application/json"
                                 },
                                 data={

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
                                     "Authorization": "Basic YzI0MzYwY2ZhYzBhMGM0MGM1MTg0MDVmNmJjNjhjYjA6MTUyNmZlYzAxYjVkMTFmNGRmNGYyMTYwNjI3Y2UzNTE=",
                                     "Content-Type": "application/json"
                                 },
                                 data={
                                     "order": {
                                         "currency": "RUB",
                                         "amount": order.price,
                                         "description": "Тестовый платеж",
                                         "id": order.id
                                     },
                                     "settings": {
                                         "terminal_id": 45,
                                         "payment_method": "card",
                                         "success_url": "https://example.com/success",
                                         "fail_url": "https://example.com/error"
                                     },
                                     "custom_parameters": {},
                                     "receipt": receipt,
                                     "trtype": 1
                                 })

        return response.json()
