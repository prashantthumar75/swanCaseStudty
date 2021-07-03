from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from .models import Item, OrderItem


@shared_task
def send_email_task(request_id):
    out_of_stock = Item.objects.filter(out_of_stock=True)
    quantity = OrderItem.objects.all().filter(user__id=request_id)

    All_Item = []
    for qu in quantity:
        All_Item.append(qu.item)
        qu.quantity = 0 # remove all items from cart
        qu.save()
    removed_ofs = []
    for itm in All_Item:
        for ofs in out_of_stock:
            if ofs == itm:
                items = ofs
                removed_ofs = All_Item
                removed_ofs.remove(items)
    user = User.objects.all().filter(id=request_id)
    user_email = user[0].email

    if not len(out_of_stock):
        print('Order conform')
        mail = EmailMessage(
            # subject
            "Your Order Conform",
            # message
            ' This is confomation email, your items are '+ str(All_Item)+' ready to dispatch\n\n',
            # from_email
            settings.EMAIL_HOST_USER,
            # recipient_list
            [user_email]
        )
        mail.send()
    else:
        print('out of stock')
        mail = EmailMessage(
            # subject
            "Out OF STOCK",
            # message
            'some products are out of stock, this list '+ str(removed_ofs) +' are ready to dispatch\n\n',
            # from_email
            settings.EMAIL_HOST_USER,
            # recipient_list
            [user_email]
        )
        mail.send()
    return None