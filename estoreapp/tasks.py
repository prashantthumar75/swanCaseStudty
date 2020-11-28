from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import SafeMIMEText, EmailMessage
from django.conf import settings

from .models import Item

@shared_task
def send_email_task(subect,message,From,To):
    out_of_stock = Item.objects.filter(out_of_stock=True)
    print(out_of_stock)

    if not len(out_of_stock):
        print('Order conform')
        mail = EmailMessage(
            # subject
            "Your Order Conform",
            # message
            ' your item comes here \n\n',
            # from_email
            settings.EMAIL_HOST_USER,
            # recipient_list
            ['parthardeshana82@gmail.com']
        )
        # mail.send()
    # send_mail(subect,message,From,[To])
    else:
        print('out of stock')
        mail = EmailMessage(
            # subject
            "Out OF STOCK",
            # message
            'Your item is out of stock\n\n',
            # from_email
            settings.EMAIL_HOST_USER,
            # recipient_list
            ['parthardeshana82@gmail.com']
        )
        # mail.send()

    return None