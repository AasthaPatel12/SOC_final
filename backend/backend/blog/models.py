from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    image=models.ImageField(upload_to='post_pics', blank=True)
    def __str__(self) :
        return self.title
    def  get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})    
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()

    def total_comment(self):
        return self.comment_set.count()

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comment_set')
    comment=models.TextField(max_length=400)
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User, on_delete=models.CASCADE, default="1")

    class Meta:
        ordering=['date_posted']

    def __str__(self):
        return self.comment[:60]

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    


