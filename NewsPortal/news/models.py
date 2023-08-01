from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(ratingPost=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('ratingPost')

        comment_rat = self.authorUser.comment_set.aggregate(ratingComment=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('ratingComment')

        self.ratingAuthor = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

class Category(models.Model):
    nameCat = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.nameCat

class Post(models.Model):
    authorPost = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    datePost = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, default='Новая публикация')
    textPost = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.textPost[0:123]}...'

    def __str__(self):
        return f'{self.title}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    textComment = models.TextField()
    dateComment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
