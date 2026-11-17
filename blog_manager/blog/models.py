from django.db import models
from django.conf import settings

class News(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news'
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='news_images/')


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.full_name} on {self.news.title}'
