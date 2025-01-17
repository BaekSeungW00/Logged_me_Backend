from __future__ import annotations

import re

from uuid import uuid4
from django.db import models

from user.models import User

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    content = models.CharField(max_length=2000)
    tagged_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='tagged_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_set: models.QuerySet[Comment]
    savedpost_set: models.QuerySet[SavedPost]
    likedpost_set: models.QuerySet[LikedPost]
    postimage_set: models.QuerySet[PostImage]
    hashtaggedpost_set: models.QuerySet[HashTaggedPost]

    def save(self, *args, **kwargs) -> None:
        super(Post, self).save(*args, **kwargs)
        self.hashtaggedpost_set.all().delete()
        for word in set(re.findall(r"#(\w+)", self.content)):
            try:
                hashtag = HashTag.objects.get(name=word)
            except HashTag.DoesNotExist:
                hashtag = HashTag(name=word)
                hashtag.save()
            HashTaggedPost.objects.get_or_create(
                post=self,
                hashtag=hashtag,
            )


class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()
    image = models.FileField(upload_to='post/images')


class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'post']]


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class HashTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200, blank=False)

    hashtaggedpost_set: models.QuerySet[HashTaggedPost]


class HashTaggedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
