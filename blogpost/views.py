from django.urls import reverse_lazy, reverse
from blogpost.forms import BlogPostForm
from blogpost.models import BlogPost
from blogpost.services import get_article_cache
from config import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)


class BlogPostListView(ListView):
    model = BlogPost

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if settings.CACHE_ENABLED:
            context_data['blogpost_list'] = get_article_cache()
        else:
            context_data['blogpost_list'] = BlogPost.objects.all()
        return context_data


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    permission_required = 'blogpost.add_blogpost'
    success_url = reverse_lazy('blogpost:blogpost_list')


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    permission_required = 'blogpost.change_blogpost'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogpost:blogpost_detail', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    permission_required = 'blogpost.delete_blogpost'
    success_url = reverse_lazy('blogpost:blogpost_list')
