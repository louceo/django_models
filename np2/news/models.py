from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

    def update_rating(self):
        # user post rating
        self.user_rating = 0
        for post_rating in Post.objects.filter(author__user = self.user).values('post_rating'):
            self.user_rating += post_rating['post_rating']
        self.user_rating *= 3
        # author comment ratings
        for author_comment_rating in Comment.objects.filter(user = self.user).values('comment_rating'):
            self.user_rating += author_comment_rating['comment_rating']
        # comment ratings from all users in author posts, except self user
        for comment_rating in Comment.objects.filter(post__author__user = self.user).values('comment_rating').exclude(user = self.user):
            self.user_rating += comment_rating['comment_rating']
        self.save()
             
    def __str__(self):
        return f'{self.user}'

    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):

    news_post = 'PO'
    article = 'AR'

    TYPES = [
        (news_post, 'Новость'),
        (article, 'Статья')
    ]
    header = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    post_rating = models.FloatField(default=0.0)
    post_type = models.CharField(max_length=2, choices=TYPES, default=news_post)
    time_in = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(to='Category', through='PostCategory', related_name='category')

    def like(self): 
        self.post_rating += 1
        self.save()
    
    def dislike(self):
        self.post_rating -= 1
        self.save()
    
    def preview(self):
        if len(self.content)>124:
            return f'{self.content[:124]}...'
        return self.content

    def __str__(self):
        return f'{self.header.title()}'

    def get_absolute_url(self):
        return reverse('news:news')


class Comment(models.Model):
    content = models.TextField(blank=True)
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ONE TO MANY USER 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self): 
        self.comment_rating += 1
        self.save()
    
    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.content} [USER: {self.user}]'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)