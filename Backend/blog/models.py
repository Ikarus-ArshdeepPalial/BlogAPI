from django.db import models
import uuid 
import os 
import random
from django.templatetags.static import static


from django.utils.text import slugify

default_images = [
    "defaults/default1.jpg",
    "defaults/default2.jpg",
    "defaults/default3.jpg",
]

# thumbnail image
def blog_random_default_thumbnail_path():
    """Pick random default images"""
    return random.choice(default_images)

def blog_thumbnail_image_file_path(instance, filename):
    """Set uploaded thumbnail path in media"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    # Truncate the slug to a maximum of 50 characters
    slug = slugify(instance.name)[:50]

    return os.path.join("uploads", "blogs", slug, "thumbnail", filename)

# content images
def blog_content_image_file_path(instance , filename):
    """Set uploaded content image path in media"""
    ext = os.path.splitext(filename)[1]

    filename = f"{uuid.uuid4()}{ext}"
    instance.name = filename

    return os.path.join("uploads", "blogs", "content_images" ,f"{filename}")


class Blog(models.Model):
    name = models.CharField(max_length=255 , default='Blog name' , blank=False , null=False)
    content = models.TextField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="blogs"
    )
    thumbnail = models.ImageField(upload_to=blog_thumbnail_image_file_path, max_length=500)
    summary = models.TextField(blank=True, null=True , default="blog is too short for summary")
    category = models.CharField(max_length=100, blank=True)

    def get_thumbnail_image_url(self):
        """Return the profile image URL or a random static default"""
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return static(blog_random_default_thumbnail_path())
        
    def __str__(self):
        return str(self.summary)
    
class BlogContentImage(models.Model):
    name = models.TextField(null=False, blank=False, unique=True)
    image = models.ImageField(upload_to = blog_content_image_file_path)

    def get_image_path(self,filename):
        image = self.clean_fields(filename)
        return image.url

    def __str__(self):
        return self.name

