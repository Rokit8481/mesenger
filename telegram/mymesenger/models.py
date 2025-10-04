from django.db import models
from autoslug import AutoSlugField

class Profile(models.Model):
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, default='default_icons/default.png')
    name = models.CharField(max_length = 100, null=False, blank=False)
    lastname = models.CharField(max_length = 100, null=True, blank=True)
    username = models.CharField(max_length = 100, null=False, blank=False, unique=True)
    bio = models.CharField(max_length = 500, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='username', unique=True)

    def __str__(self):
        return self.username


class Chat(models.Model):
    users = models.ManyToManyField(Profile, related_name='chats', blank=False)
    

class Message(models.Model):
    pass

class Attachment(models.Model):
    pass

class Reaction(models.Model):
    pass