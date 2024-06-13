from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import generate_qr_code


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        qr_code_image = generate_qr_code(instance.id)
        qr_code_path = f'qr_codes/{instance.username}_qr.png'
        user_profile.qr_code.save(qr_code_path, qr_code_image)
        user_profile.save()
    else:
        instance.userprofile.save()
