import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email_verificado = models.BooleanField(default=False)
    token_verificacion = models.UUIDField(default=uuid.uuid4, editable=False)
    token_expira_en = models.DateTimeField(null=True, blank=True)

    def generar_token_verificacion(self):
        self.token_verificacion = uuid.uuid4()
        self.token_expira_en = timezone.now() + timedelta(hours=24)
        self.save(update_fields=["token_verificacion", "token_expira_en"])
        return self.token_verificacion

    def token_es_valido(self):
        if not self.token_expira_en:
            return False
        return timezone.now() < self.token_expira_en

    def verificar_email(self):
        self.email_verificado = True
        self.token_expira_en = None
        self.save(update_fields=["email_verificado", "token_expira_en"])

    def __str__(self):
        return f"Profile({self.user.username})"


@receiver(post_save, sender=User)
def crear_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
