from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #BINA USER KE TWEET NA HOPAYE 
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/',blank=True,null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name="likeunlike",blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
    

    
