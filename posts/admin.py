from django.contrib import admin

# Register your models here.
"""Posts admin classes"""
#Django
from django.contrib import admin

#Models
from posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'title','photo',)
    list_display_links = ('pk', 'user',)
    list_editable = ('title', 'photo',)
    search_fields = ('user__username','title',)
    readonly_fields = ('created', 'modified')