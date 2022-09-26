from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    

    def __str__(self):
        return self.user.username


# # resizing images
# def save(self, *args, **kwargs):
#     super().save(*args, **kwargs)

#     if self.self.avatar:
#         img = Image.open(self.avatar.path)

#         if img.height > 100 or img.width > 100:
#             new_img = (100, 100)
#             img.thumbnail(new_img)
#             img.save(self.avatar.path)


# def save(self):
#         super().save()

#         img = Image.open(self.image.path) # Open image

#         # resize image
#         if img.height > 100 or img.width > 100:
#             output_size = (100, 100)
#             img.thumbnail(output_size) # Resize image
#             img.save(self.avatar.path)
# def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         img = Image.open(self.image.path)
#         if img.mode in ("RGBA", "P"): img = img.convert("RGB")
#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.avatar.path)