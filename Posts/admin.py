from django.contrib import admin
from .models import Post, Comment, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)