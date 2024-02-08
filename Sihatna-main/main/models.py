from django.db import models
from django.utils.text import slugify
from accounts.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class Forum(models.Model):
    
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    image = models.ImageField(upload_to='forums', blank=True)

    class Meta:
        verbose_name_plural = "forums"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Forum, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })
    
    @property
    def num_posts(self):
        return Post.objects.filter(forum=self).count()

    @property
    def last_post(self):
        return Post.objects.filter(forum=self).latest("date")


class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    approuved = models.BooleanField(default=False)

    def save(self, *args, **kwargs ):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("post", kwargs={
            "slug":self.slug
        })

    @property
    def num_replies(self):
        return Reply.objects.filter(post=self).count()
    
    @property
    def last_reply(self):
        return Reply.objects.filter(post=self).latest("date")



class Reply(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "replies"

    def __str__(self):
        return self.content[:100]
