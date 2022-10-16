from django.db import models

# Create your models here.

class RequestDetails(models.Model):
    RequestId = models.AutoField(primary_key = True)
    AddressFrom = models.CharField(max_length = 500)
    AddressTo = models.CharField(max_length = 500)
    ClientID = models.CharField(max_length = 500)
    ReceiverID = models.CharField(max_length = 500)
    ExecutiveID = models.CharField(max_length = 500)
    Status = models.CharField(max_length = 50)
    AssetSensitivity = models.CharField(max_length = 50)
    AssetType = models.CharField(max_length = 50)