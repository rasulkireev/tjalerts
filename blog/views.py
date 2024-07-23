from datetime import datetime

from django.views.generic import ListView

from blog.models import BlogPost
from utils.constants import HIRABLE_TECH_LIST_SLUGS


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status="PUBLISHED")
    template_name = "blog/blog-post-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["hirable_tech_list"] = HIRABLE_TECH_LIST_SLUGS
        context["current_year"] = datetime.now().year
        context["current_month_str"] = datetime.now().strftime("%B")
        context["current_month"] = datetime.now().month

        return context
