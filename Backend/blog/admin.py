from django.contrib import admin
from blog.models import Blog
from blog.models import BlogContentImage

admin.site.register(Blog)
admin.site.register(BlogContentImage)