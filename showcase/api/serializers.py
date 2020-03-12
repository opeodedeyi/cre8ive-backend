from rest_framework import serializers
from ..models import Showcase, Comment, ReplyComment, Collaborator
from django.utils import timezone
from django.contrib.auth import get_user_model
import math


User = get_user_model()

class CollaboratorSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    user = serializers.SlugRelatedField(slug_field='slug', queryset=User.objects.all())

    class Meta:
        model = Collaborator
        exclude = ['created_on', 'updated_on']

    def validate_user(self, value):
        showcase = self.context.get('post')
        if showcase.collaborated_showcases.filter(user=value).exists():
            raise serializers.ValidationError("Cannot add an the collaborator because the collaborator already exist")
        return value

    def create(self, validated_data):
        validated_data['post'] = self.context['post']
        return super(CollaboratorSerializer, self).create(validated_data)


class CollaboratorUpdateSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    user = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Collaborator
        exclude = ['created_on', 'updated_on']
        read_only_fields = ('pk',)



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
        return instance.user==instance.comment.showcase.user

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
        exclude = ['showcase', 'voters', 'updated_at']

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B %Y ; %H:%M:%S %Z")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_is_owner(self, instance):
        request = self.context.get("request")
        return instance.user==request.user

    def get_comment_by_op(self, instance):
        return instance.user==instance.showcase.user

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


class ShowcaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    created_on = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Showcase
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


class ShowcaseDetaiedSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    voters = serializers.SlugRelatedField(read_only=True, slug_field='slug', many=True)
    created_on = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Showcase
        exclude = ['updated_on', 'id', 'administrator']

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


class ShowcaseAdminSerializer(serializers.ModelSerializer):
    administrator = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=User.objects.all())

    class Meta:
        model = Showcase
        fields = ['administrator',]

    def update(self, instance, validated_data):
        users = validated_data.get('administrator')
        for user in users:
            instance.administrator.add(user)
        return instance


class ShowcaseLikeSerializer(serializers.ModelSerializer):
    voters = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=User.objects.all())

    class Meta:
        model = Showcase
        fields = ['voters',]
