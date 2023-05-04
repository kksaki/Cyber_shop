from celery import shared_task, Celery
from django.core.mail import send_mail
from .models import Order
from .celery import app

# app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
               Your order id is {}.'.format(order.first_name,
                                            order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@bigcart.com',
                          [order.email])
    return mail_sent