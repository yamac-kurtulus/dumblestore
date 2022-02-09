from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from .models import Movie


@receiver(post_delete, sender=Movie, dispatch_uid="post_deleted")
def object_post_delete_handler(sender, **kwargs):
    cache.clear()


@receiver(post_save, sender=Movie, dispatch_uid="post_updated")
def object_post_save_handler(sender, **kwargs):
    cache.clear()
