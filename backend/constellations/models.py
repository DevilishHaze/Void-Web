from django.db import models
class Constellation(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    ra = models.FloatField(verbose_name="Долгота,прямое восхождение (ra)", blank=False)
    dec = models.FloatField(verbose_name="Широта,склонение (dec)", blank=False)
    class Meta:
        verbose_name = 'Созвездие'
        verbose_name_plural = 'Cозвездия'

    def __str__(self):
        return self.name
