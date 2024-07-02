import logging
import random

from celery import shared_task
from django.conf import settings

from emails.models import EmailLog

logger = logging.getLogger(__name__)


@shared_task
def send_email_via_mailchimp(email, user_name):
    api_key = settings.MAILCHIMP_API_KEY
    template_name = settings.MAILCHIMP_TEMPLATE_NAME
    message_id = f'register_{email}'
    logger.info(f'Attempting to send email to {email} for user {user_name}')
    if EmailLog.objects.filter(message_id=message_id,
                               status='success').exists():
        logger.info(f'Email already successfully sent to {email}')
        return
    try:
        response = {
            'email': email,
            'status': random.choice(['sent', 'queued', 'rejected']),
            '_id': 'example_id'
        }
        logger.info(f'Mailchimp response: {response}')
        if response['status'] == 'sent':
            EmailLog.objects.create(email=email, status='success',
                                    message_id=message_id)
            logger.info(f'Email successfully sent to {email}')
        else:
            EmailLog.objects.create(email=email, status='failed',
                                    message_id=message_id)
            logger.info(f'Failed to send email to {email},'
                        f'status: {response["status"]}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        EmailLog.objects.create(email=email, status='failed',
                                message_id=message_id)


@shared_task
def retry_failed_emails():
    failed_emails = EmailLog.objects.filter(status='failed')
    for email_log in failed_emails:
        send_email_via_mailchimp.delay(email_log.email, 'retry')
        email_log.status = 'retrying'
        email_log.save()
