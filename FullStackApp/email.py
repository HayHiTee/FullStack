
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from FullStack.settings import DEFAULT_FROM_EMAIL


def send_email(subject, body, to_email):
    send_mail(
        subject,
        body,
        DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )


# Email function that sends order details to customer
def send_order_email(to_email, tracking_id, request):
    subject = 'Account Creation'
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure else 'http'
    html_message = render_to_string('FullStackApp/order_email.html',
                                    {'tracking_id': tracking_id,
                                     'domain': domain, 'protocol': protocol})
    print(html_message)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    # send_email(subject, email_msg, to_email)


# Email function that account details to new user
def send_email_account_created(to_email, username, password, request):
    subject = 'Account Creation'
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure else 'http'
    html_message = render_to_string('FullStackApp/account_email.html',
                                    {'username': username, 'password': password,
                                     'domain': domain, 'protocol': protocol})
    print(html_message)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    # send_email(subject, email_msg, to_email)