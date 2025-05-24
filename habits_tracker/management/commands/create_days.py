from django.core.management import BaseCommand, call_command

from habits_tracker.models import Day


class Command(BaseCommand):
    help = "Creates days of week."

    def handle(self, *args, **kwargs):
        Day.objects.all().delete()

        call_command("loaddata", "weekdays_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Weekdays creation finished successfully."))
