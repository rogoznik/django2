from django.core.management import BaseCommand

from authapp.models import ShopUser
from authapp.models import ShopUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            user_profile = ShopUserProfile.objects.create(user=user)
            user_profile.save()
