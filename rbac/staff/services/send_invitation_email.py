from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_invitation_email(*, request, invitation):
    """
    Emails the invitee a link containing the Invitation.token, which the
    frontend will submit back to the acceptInvitation mutation along with
    the password they choose. This is deliberately separate from
    identity.send_verification_email — that flow verifies email ownership
    for an existing logged-in user; this flow onboards a brand-new,
    not-yet-active staff account.
    """
    frontend_base = getattr(settings, "FRONTEND_URL", None)
    if frontend_base:
        accept_url = f"{frontend_base.rstrip('/')}/accept-invitation?token={invitation.token}"
    else:
        # Fallback if FRONTEND_URL isn't configured yet — build off the current request.
        accept_url = request.build_absolute_uri(f"/accept-invitation?token={invitation.token}")

    subject = f"You've been invited to join {invitation.company.name}"
    message = render_to_string(
        "staff/invitation_email.txt",
        {"invitation": invitation, "accept_url": accept_url},
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invitation.email],
    )
    return True