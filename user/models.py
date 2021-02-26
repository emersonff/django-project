from django.db import models
from django.contrib.auth.models import  AbstractUser
from imagekit.models import ProcessedImageField # used to save processed images
from imagekit.processors import  ResizeToFill

# Create your models here.
class OtherUser(AbstractUser):
    """"""
    link = models.URLField(blank = True)
    avatar = ProcessedImageField(upload_to = "avatar/%Y/%m/%d",
                                 default = "avatar/default.png",
                                 processors = [ResizeToFill(80,80)])
    
    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.username