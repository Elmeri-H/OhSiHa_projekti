from django.db import models

# Create your models here.

class Skeittispotti(models.Model):
    Nimi = models.CharField(max_length=200)
    Kaupunginosa = models.CharField(max_length=200)
    Sijainti = models.CharField(max_length=200)
    def __str__(self):
        return self.Nimi, self.Kaupunginosa, self.Sijainti
