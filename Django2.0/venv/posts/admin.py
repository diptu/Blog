from django.contrib import admin
from .models import Post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title','updated','timestamp')
    list_display_links = ['title','updated','timestamp']
    list_filter = ('title', 'content')
    ordering = ['updated']
    search_fields = ['content']
    readonly_fields = ('timestamp',)
    #autocomplete_fields = ['content']
    date_hierarchy  =   'timestamp'
    class Meta:
        model = Post

admin.site.register(Post,PostModelAdmin)
