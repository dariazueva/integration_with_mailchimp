from django.contrib.auth.models import User
from django.test import TestCase

from emails.models import EmailLog
from emails.tasks import retry_failed_emails


class UserSignalTestCase(TestCase):
    def test_user_creation_triggers_signal(self):
        user_email = 'testuser@example.com'
        User.objects.create_user(username='testuser', email=user_email,
                                 password='password')
        email_log = EmailLog.objects.get(email=user_email)
        self.assertIn(email_log.status, ['success', 'failed'],
                      'Некорректный статус записи в EmailLog')


class RetryFailedEmailsTestCase(TestCase):
    def test_retry_failed_emails(self):
        user_email = 'testuser@example.com'
        failed_log = EmailLog.objects.create(email=user_email, status='failed',
                                             message_id='example_message_id')
        retry_failed_emails()
        failed_log.refresh_from_db()
        self.assertEqual(failed_log.status, 'retrying')
