from django.db import models
from jsonfield import JSONField
import uuid


class Provider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    language = models.CharField(max_length=5)
    currency = models.CharField(max_length=3)

    class Meta:
        db_table = "provider"

class ServiceArea(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()   
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    poly = JSONField()

    class Meta:
        db_table = "service_area"
