from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_user_string
from .models import Profile
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    print("Created: ", created)
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def add_slug_to_user(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.name)
        slug_id = slugify(instance.id)
        random_string = generate_user_string()
        instance.slug = slug + "-" + random_string
        print(instance)


# this signal below helps google pass the name as an extra parameter
@receiver(pre_social_login)
def populate_user(request, sociallogin, **kwargs):
    if sociallogin.account.provider == "google":
        extra_data = sociallogin.account.extra_data
        sociallogin.user.name = extra_data['name']
        sociallogin.user.picture = extra_data['picture']