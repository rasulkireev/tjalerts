from django.views.generic import DetailView, ListView

from blog.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status=BlogPost.PUBLISHED)
    template_name = "blog/blog-post-list.html"


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog-post-detail.html"
