from django.db import models

# Create your models here.
class User(models.Model):

    class Meta:
        db_table = 'user'

    username = models.CharField(max_length=120, null=False)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=260, null=False)