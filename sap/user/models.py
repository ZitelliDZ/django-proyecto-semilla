from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


from django.template.defaultfilters import slugify
import os
# Create your models here.


class Domicilio(models.Model):

    calle = models.CharField(max_length=200)
    no_calle = models.IntegerField()
    pais = models.CharField(max_length=50)

    def __str__(self):
        return f'Domicilio {self.id}: {self.calle} {self.no_calle} {self.pais}'




# Create your models here.
class CustomUser(AbstractUser):

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Users',slugify(self.username), instance)
        return None
    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    
    email = models.EmailField(unique=True)

    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    image = models.ImageField(default='default/user.jpg',upload_to=image_upload_to ,max_length=255)

    def __str__(self):
        return f'Persona ID: {str(self.id)} - Nombre: {self.username}'