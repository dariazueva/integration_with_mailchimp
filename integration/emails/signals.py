import logging
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .tasks import send_email_via_mailchimp

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_email_via_mailchimp.delay(instance.email, instance.username)
        logger.info(f"Signal received for user: {instance.email}")
