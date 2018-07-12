from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        user_obj = User.objects.get(username=instance)
        token_obj = Token.objects.get(user=user_obj)
        user_obj.token = str(token_obj.key)
        user_obj.save()


class User(AbstractUser):
    class Meta:
        db_table = 'users'
        unique_together = ('email',)

    addedBy = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username