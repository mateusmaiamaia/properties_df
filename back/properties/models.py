from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    sqm_price = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    link = models.URLField()

    class Meta:
        db_table = 'properties' 

    def __str__(self):
        return self.title
