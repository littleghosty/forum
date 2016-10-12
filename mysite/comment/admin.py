from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "status", "article")

admin.site.register(Comment, CommentAdmin)
