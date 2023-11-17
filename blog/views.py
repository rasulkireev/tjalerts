from django.views.generic import ListView

from utils.constants import HIRABLE_TECH_LIST

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status="PUBLISHED")
    template_name = "blog/blog-post-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["hirable_tech_list"] = HIRABLE_TECH_LIST

        return context
