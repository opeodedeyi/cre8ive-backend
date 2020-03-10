from django.db import models
from django.conf import settings
from accounts.models import Skill

class Collaborate(models.Model):
    '''
    collaborate mmodel, that allows users to post about 
    projects he wants to undertake, and aks for peole interested
    with relevant skills to show their interest
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="collaborator_user")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    media = models.TextField(null=True)
    location = models.CharField(null=True, max_length=100)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likers")
    administrator = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="adminis", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    '''
    Comment model, people will be able to comment on the collaborate
    model above, and the comments can be upvoted
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(null=False)
    post = models.ForeignKey(Collaborate, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE,  related_name="commentator")
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comment_likers")

    def __str__(self):
        return self.user.name


class ReplyComment(models.Model):
    '''
    Reply model, people will be able to reply to the comment
    model above, and the reply can be upvoted
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply_comment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE, related_name="reply_user")
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="replylikes")

    def __str__(self):
        return self.user.name


class Interest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="interest_user")
    post = models.ForeignKey(Collaborate, on_delete=models.CASCADE, related_name="interest_collaborate")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
