from django.contrib import admin
from .models import Showcase, Comment, ReplyComment, Collaborator

admin.site.register(Showcase)
admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Collaborator)