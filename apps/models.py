from datetime import datetime
from PIL import Image
from django.db.models.signals import post_save 
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
        
        category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
        image=models.ImageField(upload_to="images/'%Y-%m-%d %H-%M-%S'")
        price=models.IntegerField()

        def __str__(self):
            return str(self.category)
        @staticmethod
        def get_all_products_by_id(category_id):
            if category_id:
                return Product.objects.filter(category=category_id)
            else:
                return Product.objects.all()
        def save(self):
            super().save()  # saving image first
            img = Image.open(self.image.path) # Open image using self

            if img.height > 300 or img.width > 300:
                 new_img = (300, 300)
                 img.thumbnail(new_img)
                 img.save(self.image.path)  # saving image at the same path        


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
   
    mobile_no=models.CharField(max_length=10)

    
    def __str__(self):
        return "Profile  {}" .format(self.user.username)
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        
    post_save.connect(create_user_profile, sender=User)
    