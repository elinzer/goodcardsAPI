from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=120)
    color_identity = models.CharField(max_length=10)
    card_type = models.CharField(max_length=120)
    rarity = models.CharField(max_length=50)
    mtg_set = models.CharField(max_length=3)
    text = models.TextField(max_length=2000)
    image_url = models.URLField(max_length=1000)
    
    
def __str__(self):
    return self.name
