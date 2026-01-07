from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog
from .blog_ai_utils.Generate_summary import generate_summary
from .blog_ai_utils.Blog_category import get_category

@receiver(post_save, sender=Blog)
def populate_summary_and_category(sender, instance, created, **kwargs):
    """
    Automatically populates the summary and category for a new blog post.
    """
    if created:
        summary = generate_summary(instance.content)
        category = get_category(instance.content)
        Blog.objects.filter(pk=instance.pk).update(summary=summary, category=category)
