from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_email_task(self, *, subject, message, recipient_list):
    """
    Shared by identity (verification/reset codes) and staff (invitations) —
    any Django-sendable plain-text email goes through here so SMTP latency
    and transient failures never block the request/response cycle inside
    a GraphQL mutation.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
    )