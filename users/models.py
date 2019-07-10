from django.db import models
from django.contrib.auth.models import User
from PIL import Image#pillow lib which we installed earlier which do all image stuffs

class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE) #onetoone relationship..
	                                                          #1 user will have only one profilepic and image
	                                                          #we directly can use 
	                                                          #user=User.objects.all().first()
	                                                          #then directly can use user.profile.image.url
	                                                          #in profile.html it is used
	                                                          #profile will be object of Profile class
	                                                          #dont know how
	image=models.ImageField(default='default.jpg',upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'
