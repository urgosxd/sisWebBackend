from datetime import datetime
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
import json

# Create your models here.

class Document(models.Model):
    Extension = models.CharField(max_length=40, null=True)
    FileName = models.CharField(max_length=200, null=True)
    Doc_Content = models.BinaryField(null=True)
    class Meta:
        abstract=True
class Notification(models.Model):
    message = models.CharField(max_length =300,null=False,blank=False)

class Tour(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    excursion = models.CharField(max_length =100,null=False,blank=False)
    provedor = models.CharField(max_length =100,null=False,blank=False)
    ppp = models.DecimalField(max_digits=8, decimal_places=2)
    pvp = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()
def NicePrintInstance(instance):
    values = [(k,v) for k,v in instance.__dict__.items() if k != '_state']
    return values

@receiver(post_save,sender=Tour)
def createNotification(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un tour de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un tour {NicePrintInstance(instance)}  a las {currentTime}")


@receiver(pre_save,sender=Tour)
def getUpdateNotification(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Tour)
def getDeleteNotification(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un tour de {NicePrintInstance(instance)} a las {currentTime}")
    

class FichaTecnica(Document):
    Tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name="fichasTecnicas",null=True)



