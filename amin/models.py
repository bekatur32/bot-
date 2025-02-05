# models.py
from django.db import models

class Tovar(models.Model):
    name = models.CharField(max_length=255)
    price_sng = models.PositiveIntegerField()
    price_EUROPE_AMERICA = models.PositiveIntegerField()
    price_Africa_Australia = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True,default='products/default_image.png')
    category = models.CharField(max_length=100, choices=[('fight_katan', 'Боевые катаны'), ('katan_replic', 'Не боевые катаны'),('exclusive', 'экслюзвный товар')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
