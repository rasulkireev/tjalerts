from django.core.management import call_command


def vacuum_analyze():
    call_command("vacuum_analyze")
