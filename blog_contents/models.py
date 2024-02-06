from django.db import models
from Accounts.models import User
# from comments.models import Comments
# Create your models here.
    

"""categrie name """
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return self.category_name

"""sub categories"""
class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=300)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.sub_category_name
    
    
"""blog sessions"""
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    header = models.CharField(max_length=300,null=True)
    about = models.CharField(max_length=1000,null=True)
    body = models.CharField(max_length=20000,null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True)
    conclusion = models.CharField(max_length=1000, null=True)
    images = models.ImageField(upload_to='blog_images/',null=True)
    likes = models.IntegerField(default=0,null=True)

    
    def __str__(self) -> str:
        return self.header
    

"""comments session"""
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    comments = models.CharField(max_length=400, blank=True, null=True)
    like = models.IntegerField(default=0)
    

    def __str__(self) -> str:
        return self.comments
"""reply sessions"""
class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    Comments = models.ForeignKey(Comments, null=True, on_delete=models.CASCADE)
    reply_comment = models.CharField(max_length=300,null=True,blank=True)
    replay_auther = models.ForeignKey("self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE)