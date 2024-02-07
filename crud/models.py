from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)

# Create your models here.

class Document(models.Model):
    Extension = models.CharField(max_length=40, null=True)
    FileName = models.CharField(max_length=200, null=True)
    Doc_Content = models.BinaryField(null=True)
    class Meta:
        abstract=True
class Notification(models.Model):
    message = models.CharField(max_length =100,null=False,blank=False)

class Tour(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    excursion = models.CharField(max_length =100,null=False,blank=False)
    provedor = models.CharField(max_length =100,null=False,blank=False)
    ppp = models.DecimalField(max_digits=8, decimal_places=2)
    pvp = models.DecimalField(max_digits=8, decimal_places=2)

@receiver(post_save,sender=Tour)
def get_Notification(sender,instance,created,**kwargs):
    if not created:
        return 
    print(instance.id)
    print(datetime.now())
    print(get_current_user())
    print(get_current_authenticated_user())
    
    
class FichaTecnica(Document):
    Tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name="fichasTecnicas",null=True)



