from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('1', 'Editor'),
        ('2', 'Author'),
        ('3', 'Subscriber'),]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='3')

class PostData(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    author_id = models.ForeignKey(
        "CustomUser",
        # related_name='blogs'
        on_delete=models.CASCADE,)
    published = models.BooleanField(default=False)
    published_on = models.DateField()
    tags = ArrayField(models.CharField(max_length=50), blank=True)

class PostComments(models.Model):
    post_id = models.ForeignKey(
        "PostData",
        on_delete=models.CASCADE,)
    author_id_sub = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,)
    content = models.TextField()
    DataTime = models.DateTimeField()
    seen = models.BooleanField(default=False, blank=True)