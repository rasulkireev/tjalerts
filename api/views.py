from typing import List, Optional

from django.db.models import Count, Q
from django_q.tasks import async_task
from ninja import NinjaAPI, Query

from hn_jobs.utils import get_tjalerts_logger
from jobs.models import Company, Email, Post, Technology
from jobs.tasks import create_valid_emails

from .schemas import ReadCompany, ReadEmails, TechnologySchema

logger = get_tjalerts_logger(__name__)


api = NinjaAPI()


@api.get("/companies", response=List[ReadCompany])
def companies(request):
    return Company.objects.all()


@api.get("/create-emails")
def create_emails(request):
    async_task(create_valid_emails)  # noqa: F821
    return "Task Started"


@api.get("/emails", response=ReadEmails)
def get_emails(
    request,
    is_valid: bool = True,
    with_names_only: bool = Query(False, alias="names"),
    exclude_generic_email: bool = Query(True, alias="exclude-generic"),
    only_approved: bool = Query(False, alias="only-approved"),
):
    emails = (
        Email.objects.select_related("company")
        .filter(email_is_valid=is_valid)
        .values("email", "name", "company__name", "company__compliment")
    )

    if with_names_only:
        emails = emails.exclude(name="")

    if exclude_generic_email:
        emails = emails.exclude(email_is_generic=True)

    if only_approved:
        emails = emails.filter(is_approved=True)

    unique_emails = emails.values("email").distinct()
    unique_emails_queryset = emails.filter(email__in=unique_emails)

    return {
        "count": len(unique_emails_queryset),
        "emails": list(unique_emails_queryset),
    }


@api.get("/jobs")
def get_jobs(request, technologies=Query(None)):
    posts = Post.objects.prefetch_related("company", "technologies", "titles")

    user_submitted_technologies = technologies.split(",")
    user_submitted_technologies = [item.strip() for item in user_submitted_technologies]

    posts_list = []
    for post in posts:
        post_technologies = [technology.name for technology in post.technologies.all()]

        if not set(user_submitted_technologies).issubset(post_technologies):
            continue

        post_titles = [title.name for title in post.titles.all()]

        entry = {
            "company_name": post.company.name,
            "company_url": post.company.company_homepage_link,
            "description": post.description,
            "compensation_summary": post.compensation_summary,
            "min_salary": post.min_salary,
            "max_salary": post.max_salary,
            "is_remote": post.is_remote,
            "locations": post.locations,
            "technologies": post_technologies,
            "title": post_titles,
            "id": str(post.id),
            "who_is_hiring_comment_id": post.who_is_hiring_comment_id,
            "submitted_datetime": post.submitted_datetime,
        }

        posts_list.append(entry)

    return {
        "count": len(posts_list),
        "jobs": posts_list,
    }


@api.get("/technologies/search", response=List[TechnologySchema])
def search_technologies(request, query: Optional[str] = Query(None, min_length=2)):
    if query:
        technologies = (
            Technology.objects.filter(Q(name__icontains=query) | Q(slug__icontains=query))
            .annotate(post_count=Count("posttechnology"))
            .order_by("-post_count")[:20]
        )  # Limit to 20 results, ordered by post count
    else:
        technologies = Technology.objects.none()

    return [
        TechnologySchema(id=str(tech.id), name=tech.name, slug=tech.slug, post_count=tech.post_count)
        for tech in technologies
    ]
