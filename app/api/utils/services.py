import logging
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_base_email(subject, html_template, context, recipient):
    body = render_to_string(html_template, context=context)
    message = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient, ])
    message.content_subtype = 'html'
    try:
        message.send()
    except Exception as e:
        logger.error(f"Error: {e}")
