from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Run VACUUM and ANALYZE on the database"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
            cursor.execute("ANALYZE;")
        self.stdout.write(self.style.SUCCESS("Successfully ran VACUUM and ANALYZE"))
