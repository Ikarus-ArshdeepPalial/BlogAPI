# documents.py
from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from blog.models import Blog

post_index = Index('blogs')

@registry.register_document
class BlogDocument(Document):
    class Index:
        name = 'blogs'

    class Django:
        model = Blog
        fields = [
            'name',
            'content',
            'category',
            'created_at'
        ]