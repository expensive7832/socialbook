from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomizeUser
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="profile")
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomizeUser()

    def __str__(self):
        return self.email
    
class PostImage(models.Model):
    image = models.ImageField(upload_to="posts")

    def __str__(self):
        return self.image.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    text = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    images = models.ManyToManyField(PostImage)

    def __str__(self):
        return self.text


