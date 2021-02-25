from django.db import models
from django.contrib.auth.models import  AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import  ResizeToFill

# Create your models here.
class  OtherUser(AbstractUser):
    pass