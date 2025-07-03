from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ajouter_utilisateur_au_groupe(sender, instance, created, **kwargs):
    if created and instance.role == 'elder':
        groupe, _ = Group.objects.get_or_create(name='elder')
        instance.groups.add(groupe)

    if created and instance.role == 'volunteer':
        groupe, _ = Group.objects.get_or_create(name='volunteer')
        instance.groups.add(groupe)
