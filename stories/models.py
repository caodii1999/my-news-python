from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.name

class Story(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=250,unique=True)
    author = models.CharField(max_length=250)
    url = models.URLField(null=True,blank=True)
    content = RichTextUploadingField()
    public_day = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to="stories/images",default="stories/images/default.jpg")

    def __str__(self):
        return self.name
        
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=264)
    message = models.TextField()

    def __str__(self):
        return self.name + ", " + self.subject
        
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    portfolio = models.URLField(blank=True)
    image = models.ImageField(upload_to= "stories/images", default="stories/images/people_default.png" )

    def __str__(self):
        return self.user.username

