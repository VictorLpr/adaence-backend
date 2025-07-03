from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_group(sender, instance, created, **kwargs):
    if created and instance.role == 'elder':
        group, _ = Group.objects.get_or_create(name='elder')
        instance.groups.add(group)

    if created and instance.role == 'volunteer':
        group, _ = Group.objects.get_or_create(name='volunteer')
        instance.groups.add(group)
