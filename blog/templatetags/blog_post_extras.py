from django import template
from django.db.models import Count

from hn_jobs.utils import get_tjalerts_logger
from jobs.models import Technology

logger = get_tjalerts_logger(__name__)

register = template.Library()


@register.filter()
def get_technology_name_from_slug(slug: str) -> str:
    tech = (
        Technology.objects.filter(slug__icontains=slug)
        .annotate(post_count=Count("post"))
        .order_by("-post_count")
        .first()
    )

    return tech.name
