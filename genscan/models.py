from django.db import models


# Create your models here.

class QrCode(models.Model):
    data = models.CharField(max_length=200)
    img = models.ImageField(upload_to='qr_codes',blank=True)

    def __str__(self):
        return self.data
