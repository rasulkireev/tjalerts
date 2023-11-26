from django.urls import path

from .views import HighestPaidBlogPostListView, HighestPaidJobsView

urlpatterns = [
    path("highest-paid-list", HighestPaidBlogPostListView.as_view(), name="highest-paid-blog-posts"),
    path("highest-paid-<slug:name>-jobs", HighestPaidJobsView.as_view(), name="highest-paid-job-blog-post"),
    # path("<slug:slug>", BlogPostDetailView.as_view(), name="blog-post"),
]
