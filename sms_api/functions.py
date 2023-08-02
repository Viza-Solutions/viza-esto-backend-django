import africastalking
from django.http import JsonResponse


def send_sms(message, recepient):
    username = "viza"
    api_key = "c26815e841421b75a25fa8206800dc001b347d28f6c43881d5ad1151f539137d"
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    def on_finish(error, response):
        if error is not None:
            raise error
        # print(response)

    sms.send(message, recepient, callback=on_finish)
