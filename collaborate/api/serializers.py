from rest_framework import serializers
from ..models import (Collaborate,
                      Comment,
                      Interest,
                      ReplyComment)
from django.utils import timezone
from django.contrib.auth import get_user_model
import math

User = get_user_model()

class CollaborateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    created_on = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    user_has_shown_interest = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collaborate
        exclude = ['voters', 'updated_on', 'id', 'administrator']

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_is_owner(self, instance):
        request = self.context.get("request")
        return instance.user==request.user

    def get_is_admin(self, instance):
        request = self.context.get("request")
        return instance.administrator.filter(pk=request.user.pk).exists()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_user_has_shown_interest(self, instance):
        request = self.context.get("request")
        try:
            return instance.interest_collaborate.filter(user=request.user).exists()
        except:
            return False
    
    def get_comment_count(self, instance):
        return instance.comments.count()

    def get_created_on(self, instance):
        now = timezone.now()
        diff = now - instance.created_on

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) +  "second ago"
            return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            return str(years) + " years ago"


class CollaborateAdminSerializer(serializers.ModelSerializer):
    administrator = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=User.objects.all())

    class Meta:
        model = Collaborate
        fields = ['administrator',]

    def update(self, instance, validated_data):
        users = validated_data.get('administrator')
        for user in users:
            instance.administrator.add(user)
        return instance


class CollaborationLikeSerializer(serializers.ModelSerializer):
    voters = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=User.objects.all())

    class Meta:
        model = Collaborate
        fields = ['voters',]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    created_at = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    created_when = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    comment_by_op = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        exclude = ['post', 'voters', 'updated_at']

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B %Y ; %H:%M:%S %Z")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_is_owner(self, instance):
        request = self.context.get("request")
        return instance.user==request.user

    def get_comment_by_op(self, instance):
        return instance.user==instance.post.user

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_created_when(self, instance):
        now = timezone.now()
        diff = now - instance.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) +  "second ago"
            return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            return str(years) + " years ago"


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    created_at = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    created_when = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    reply_by_op = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReplyComment
        exclude = ['comment', 'voters', 'updated_at']

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B, %Y")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_is_owner(self, instance):
        request = self.context.get("request")
        return instance.user==request.user

    def get_reply_by_op(self, instance):
        return instance.user==instance.comment.post.user

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_created_when(self, instance):
        now = timezone.now()
        diff = now - instance.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) +  "second ago"
            return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            return str(years) + " years ago"


class InterestSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    showed_interest_when = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Interest
        exclude = ['id', 'post', 'created_on']

    def get_showed_interest_when(self, instance):
        now = timezone.now()
        diff = now - instance.created_on

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            if seconds == 1:
                return str(seconds) +  "second ago"
            return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            return str(years) + " years ago"
