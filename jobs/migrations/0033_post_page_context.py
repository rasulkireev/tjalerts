from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0032_remove_company_emails_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="company_homepage_context",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="post",
            name="company_homepage_reader_content",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="post",
            name="job_posting_context",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="post",
            name="job_posting_reader_content",
            field=models.TextField(blank=True, default=""),
        ),
    ]
