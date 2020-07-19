from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save          # this we import for whenever the new user will created it will automatically created as customer


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:                                                     # if the user is newly created then we will create it's profile                
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)           # this will check the new user will save or not
