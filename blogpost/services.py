from django.core.cache import cache
from blogpost.models import BlogPost


def get_article_cache():
    key = 'client_list'
    blogpost_list = cache.get(key)
    if blogpost_list is None:
        blogpost_list = BlogPost.objects.all()
        cache.set(key, blogpost_list)
    return blogpost_list
