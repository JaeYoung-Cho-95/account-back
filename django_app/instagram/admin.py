from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class postAdmin(admin.ModelAdmin):
    list_display = ['id','message','updated_at']
    list_display_links = ['message']
    search_fields = ["message"]
    list_filter = ["updated_at"]