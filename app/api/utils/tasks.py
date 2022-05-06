from django.utils import translation
from django.utils.translation import gettext as _
from translation_template.celery import app
from app.api.utils.services import send_base_email


@app.task(bind=True, default_retry_delay=300, max_retries=5)
def send_signup_mail(*args, **kwargs):
    recipient = kwargs.get('recipient')
    language = kwargs.get('language')
    translation.activate(language)
    current_language_info = translation.get_language_info(language)
    context = {'username': recipient, 'lang': current_language_info.get('name_local')}
    html_template = 'email/sign_up_email.html'
    subject = _('Welcome on board!!!')

    send_base_email(subject, html_template, context, recipient)


@app.task(bind=True, default_retry_delay=300, max_retries=5)
def send_password_update_mail(*args, **kwargs):
    recipient = kwargs.get('recipient')
    language = kwargs.get('language')
    translation.activate(language)
    current_language_info = translation.get_language_info(language)
    context = {'username': recipient, 'lang': current_language_info.get('name_local')}
    html_template = 'email/update_password_email.html'
    subject = _('Password was changed!!!')

    send_base_email(subject, html_template, context, recipient)


@app.task(bind=True, default_retry_delay=300, max_retries=5)
def send_language_update_mail(*args, **kwargs):
    recipient = kwargs.get('recipient')
    language = kwargs.get('language')
    translation.activate(language)
    current_language_info = translation.get_language_info(language)
    context = {'username': recipient, 'lang': current_language_info.get('name_local')}
    html_template = 'email/update_language_email.html'
    subject = _('Language was changed!!!')

    send_base_email(subject, html_template, context, recipient)
