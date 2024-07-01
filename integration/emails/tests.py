from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, call

from emails.models import EmailLog
from emails.tasks import send_email_via_mailchimp, retry_failed_emails


class UserSignalTestCase(TestCase):
    @patch('emails.tasks.send_email_via_mailchimp.delay')
    def test_user_creation_triggers_signal(self, mock_send_email):
        user_email = 'testuser@example.com'
        user = User.objects.create_user(username='testuser', email=user_email,
                                        password='password')
        mock_send_email.assert_called_once()
        expected_call = call(user_email, 'testuser')
        self.assertEqual(mock_send_email.call_args, expected_call)
        result = send_email_via_mailchimp.delay(user_email, 'testuser')
        self.assertTrue(result.successful())


class RetryFailedEmailsTestCase(TestCase):
    @patch('emails.tasks.send_email_via_mailchimp.delay')
    def test_retry_failed_emails(self, mock_send_email):
        # Создаем пользователя и запись в EmailLog со статусом 'failed'
        user_email = 'testuser@example.com'
        User.objects.create_user(username='testuser', email=user_email, password='password')
        email_log = EmailLog.objects.create(email=user_email, status='failed')

        # Запускаем задачу повторной отправки
        retry_failed_emails()

        # Проверяем вызов задачи send_email_via_mailchimp.delay()
        mock_send_email.assert_called_once_with(user_email, 'retry')

        # Проверяем изменение статуса на 'retrying'
        email_log.refresh_from_db()  # Обновляем данные записи из базы данных
        self.assertEqual(email_log.status, 'retrying')
