import africastalking
from property_app.models import Room
from tenant_app.models import *
from payment_app.models import *
from .models import *
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.exceptions import ObjectDoesNotExist


def send_sms(message, recipient, client_id):
    try:
        sms_credential = SmsCredential.objects.get(client_id=client_id)
        api_key = sms_credential.api
        username = sms_credential.username

        # username = "viza"
        # api_key = "c26815e841421b75a25fa8206800dc001b347d28f6c43881d5ad1151f539137d"

        africastalking.initialize(username, api_key)
        sms = africastalking.SMS

        def on_finish(error, response):
            if error is not None:
                raise error

        sms.send(message, recipient, callback=on_finish)

    except SmsCredential.DoesNotExist:
        print(f"No SmsCredential found for client with ID {client_id}")


def sms_to_unpaid_bal():
    tenants = Tenant.objects.filter(deleted=False)
    for tenant in tenants:
        pk = tenant.id
        client_id = tenant.client.id
        current_datetime = datetime.now()

        # Get the current month and year
        current_month = int(current_datetime.month)
        current_year = int(current_datetime.year)

        try:
            queryset = PaymentTransaction.objects.filter(tenant_id=pk, reversed=False)
            # Calculate unpaid and prepaid months
            last_transaction = queryset.order_by("-id").first()
            balance = int(last_transaction.balance)
            year = int(last_transaction.year)
            month = int(last_transaction.month)

            try:
                tenant_details = Tenant.objects.get(pk=pk)
                room_id = tenant_details.room_id
                name = (
                    tenant_details.fullname
                )  # Set the 'name' variable with the tenant's name

                # Get the room object using the retrieved room_id
                room = Room.objects.get(pk=room_id)
                room_number = room.room_number
                estate = str(room.property)
                monthly_price = int(room.monthly_price)

            except Tenant.DoesNotExist:
                # Handle the case when no tenant is found for the given tenant_id
                room_id = None
                monthly_price = None
                name = "Undefined"

            # Calculate the curr_balance
            months_difference = ((current_year - year) * 12) + (current_month - month)

            curr_balance = (-months_difference * monthly_price) + balance

            if curr_balance > 0:
                pass
            else:
                curr_balance_str = "Underpaid Amount KES " + str(curr_balance) + "/="
                typee = "Underpaid"

                # print(curr_balance)
                curr_balance_str = f"{abs(curr_balance):,.2f}"  # Format balance with two decimal places

                message = (
                    f"Hello {tenant.fullname},\n\n"
                    f"This is a friendly reminder that your current outstanding balance is KES {curr_balance_str}. "
                )

                recepient = [tenant.phone_number]
                send_sms(message, recepient, client_id)
        except:
            pass


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     sms_to_unpaid_bal, "cron", month="*", day=5, hour=8, minute=30, second=0
    # )
    scheduler.add_job(sms_to_unpaid_bal, "interval", seconds=10)
    scheduler.start()


start()
