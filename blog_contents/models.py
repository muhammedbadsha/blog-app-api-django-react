from django.db import models
from Accounts.models import User

# Create your models here.

"""images session"""
class Images(models.Model):
    id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=50,null=True)
    image = models.ImageField(upload_to='blog_images/',null=True)

    def __str__(self) -> str:
        return self.image_name

"""reply sessions"""
class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True)
    reply = models.CharField(max_length=300)

"""comments session"""
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True)
    comments = models.CharField(max_length=400)
    like = models.IntegerField(default=0)
    reply = models.ForeignKey(Reply,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comments
    

"""sub categories"""
class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=300)
    def __str__(self) -> str:
        return self.sub_category_name
    

"""categrie name """
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200,null=True)
    sub_category= models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.category_name
    
    
"""blog sessions"""
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    header = models.CharField(max_length=300,null=True)
    about = models.CharField(max_length=1000)
    body = models.CharField(max_length=20000,null=True)
    conclusion = models.CharField(max_length=1000)
    images = models.ForeignKey(Images,on_delete=models.CASCADE)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    likes = models.IntegerField()

    def __str__(self) -> str:
        return self.header
    



