from django.db import models


class Constellation(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name='Латинское название')
    name_rus = models.CharField(max_length=100, verbose_name="Русское название", null=True)
    ra = models.FloatField(verbose_name="Долгота,прямое восхождение (ra)", blank=False)
    dec = models.FloatField(verbose_name="Широта,склонение (dec)", blank=False)
    image_url = models.URLField(blank=True , null=True)
    class Meta:
        verbose_name = 'Созвездие'
        verbose_name_plural = 'Cозвездия'

    def __str__(self):
        return f"{self.name} ({self.name_rus})"
