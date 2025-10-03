from django.db import models

class Property(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    
    # CORREÇÃO: Todos os campos numéricos como BigIntegerField
    price = models.BigIntegerField(null=True, blank=True)
    sqm_price = models.BigIntegerField(null=True, blank=True)  # Mudado para BigInteger
    area = models.BigIntegerField(null=True, blank=True)       # Mudado para BigInteger

    city = models.CharField(max_length=100)
    link = models.URLField()

    class Meta:
        db_table = 'properties'
        app_label = 'main'

    def __str__(self):
        return self.title