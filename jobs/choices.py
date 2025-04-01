from django.db import models


class PostSource(models.TextChoices):
    HACKER_NEWS = "Hacker News"
