from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)

admin.site.register(Comment)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

