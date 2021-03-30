from django.db import models
from django.contrib.auth.models import AbstractUser
# Custom Account Model
def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.username, filename)

class User(AbstractUser):
    image = models.ImageField(verbose_name="Profile Photo",upload_to=upload_to,blank=True)
    