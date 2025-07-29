from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = f"http://{domain}/api/users/verify-email/{uid}/{token}/" # Se puede adaptar a dominio personalizado

    subject = "Verify your email address for AI FlashLang"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    # Render HTML template (with context for the user)
    html_content = render_to_string("emails/verify_email.html", {
        "user": user,
        "verification_link": link,
    })

    # Fallback plain text (for email clients that don't support HTML)
    text_content = (
        f"Hi {user.username},\n\n"
        f"Thank you for registering with AI FlashLang!\n"
        f"Please verify your email address by clicking the following link:\n\n"
        f"{link}\n\n"
        f"If you did not create this account, please ignore this email.\n\n"
        f"— The FlashLang Team"
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        print(f"[ERROR] Failed to send verification email: {e}")