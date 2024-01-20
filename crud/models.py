from django.db import models

# Create your models here.

class Document(models.Model):
    Extension = models.CharField(max_length=50, null=True)
    FileName = models.CharField(max_length=200, null=True)
    Doc_Content = models.BinaryField(null=True)


class Tour(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    excursion = models.CharField(max_length =100,null=False,blank=False)
    provedor = models.CharField(max_length =100,null=False,blank=False)
    ppp = models.DecimalField(max_digits=8, decimal_places=2)
    pvp = models.DecimalField(max_digits=8, decimal_places=2)
    
class FichaTecnica(Document):
    Tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name="fichasTecnicas")



