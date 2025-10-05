from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(BaseModel):
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, default='default/default_icon.png')
    name = models.CharField(max_length = 100, null=False, blank=False)
    lastname = models.CharField(max_length = 100, null=True, blank=True)
    username = models.CharField(max_length = 100, null=False, blank=False, unique=True)
    bio = models.CharField(max_length = 500, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta: 
        ordering = ["created_at"]
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'


class Chat(BaseModel):
    users = models.ManyToManyField(Profile, related_name='chats', blank=False)
    background = models.ImageField(upload_to='backgrounds/', null=True, blank=True, default='default/default_bg.png')
    is_group = models.BooleanField(default=False)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title or f"Чат {self.id}"
    
    class Meta: 
        ordering = ["created_at"]
        verbose_name = 'Чат'
        verbose_name_plural = 'Чати'


class Message(BaseModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages', null=False)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.text[:30] if self.text else '[файл]'}"

    class Meta: 
        ordering = ["created_at"]
        verbose_name = 'Повідомлення'
        verbose_name_plural = 'Повідомлення'



class Attachment(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField(blank=False, null=False)

    def __str__(self):
        return f"Вкладення до повідомлення {self.message}"
    
    class Meta: 
        ordering = ["created_at"]
        verbose_name = 'Вкладення'
        verbose_name_plural = 'Вкладення'

class Reaction(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reactions', null=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    emoji = models.CharField(max_length=10, choices=[
        ("❤️", "❤️"),
        ("👎", "👎")
    ])

    def __str__(self):
        return f"{self.emoji} --- {self.message}"
    
    class Meta: 
        ordering = ["created_at"]
        verbose_name = 'Реакція'
        verbose_name_plural = 'Реакції'
        constraints = [
            models.UniqueConstraint(fields=['user', 'message', 'emoji'], name='unique_user_reaction')
        ]


