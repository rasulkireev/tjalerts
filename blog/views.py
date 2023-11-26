from django.views.generic import ListView, TemplateView

from jobs.models import Post
from utils.constants import HIRABLE_TECH_LIST

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status="PUBLISHED")
    template_name = "blog/blog-post-list.html"


class HighestPaidBlogPostListView(TemplateView):
    template_name = "blog/highest-paid-blog-post-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["hirable_tech_list"] = HIRABLE_TECH_LIST

        return context


class HighestPaidJobsView(TemplateView):
    template_name = "blog/highest-paid-jobs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["object_list"] = Post.objects.filter(technologies__name=self.kwargs.get("name")).order_by(
            "-max_salary"
        )[:20]

        return context
