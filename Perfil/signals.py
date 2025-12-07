from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender = User)
def crear_perfil(sender, instance, created, **kwards):
    if created:
        Perfil.objects.create(user=instance)



@receiver(post_delete, sender=Perfil)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()
