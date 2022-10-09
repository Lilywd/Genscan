from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class QrCode(models.Model):
    data = models.CharField(max_length=200)
    img = models.ImageField(upload_to='qr_codes',blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.data

@receiver(post_save,sender=QrCode)
def submission_save(sender, instance,save, **kwargs):
   instance.QrCode.save()



