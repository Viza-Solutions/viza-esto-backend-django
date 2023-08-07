from django.db import models
from client_app.models import Client


class SmsCredential(models.Model):
    api = models.TextField()
    username = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, unique=True)

    class Meta:
        unique_together = ["api", "client"]

    def __str__(self):
        return str(self.client)
