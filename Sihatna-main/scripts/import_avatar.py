# import_avatars.py
import random
from accounts.models import Avatar
from django.core.management import BaseCommand

def generate_avatar():
    avatars = []
    for i in range(50):
        avatar = {
            "name": f"avatar {i+1}",
            "image": random.choice(["https://api.dicebear.com/7.x/micah/svg?seed=avatar{}".format(i),
                                   "https://api.dicebear.com/7.x/miniavs/svg?seed=avtar{}".format(i),
                                   "https://api.dicebear.com/7.x/bottts/svg?seed=avatar{}".format(i),
                                   "https://api.dicebear.com/7.x/adventurer/svg?seed=avatar{}".format(i),
                                   "https://api.dicebear.com/7.x/lorelei/svg?seed=avatar{}".format(i)])
        }
        avatars.append(avatar)
    return avatars

AVATAR_CHOICES = ([(avatar['name'], avatar['image']) for avatar in generate_avatar()])

def import_avatars():
    avatars = generate_avatar()
    for avatar_data in avatars:
        Avatar.objects.get_or_create(name=avatar_data["name"], defaults={'image_url': avatar_data["image"]})

def run () :
    import_avatars()