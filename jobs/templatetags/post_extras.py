from django import template

from jobs.models import TechnologyMapping

register = template.Library()


@register.filter()
def replace_child_with_parent_technology(technology):
    child = TechnologyMapping.objects.filter(child=technology)

    if child.exists():
        technology = child.first().parent

    return technology
