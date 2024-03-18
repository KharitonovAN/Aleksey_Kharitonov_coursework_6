from django.core.mail import send_mail
from django.urls import reverse
from config import settings


def send_verify_email(user):
    domain = 'http://127.0.0.1:8000/'

    send_mail(
        subject=f'Подтверждение регистрации для {user.email}',
        message=f"""Вы зарегистрировались. Необходимо подтвердить Ваш аккаунт по ссылке \n
                    {domain}{reverse('users:confirm_registration', kwargs={'uuid': user.field_uuid})}""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
