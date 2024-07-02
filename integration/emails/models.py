from django.db import models


class EmailLog(models.Model):
    email = models.EmailField()
    status = models.CharField(max_length=20)
    message_id = models.CharField(max_length=100, unique=True,
                                  blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.status}'
