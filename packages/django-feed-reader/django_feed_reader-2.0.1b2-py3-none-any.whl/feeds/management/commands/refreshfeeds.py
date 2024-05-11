
from django.core.management.base import BaseCommand

from feeds.utils import update_feeds


class Command(BaseCommand):
    """
        This command refreshes the RSS feeds

        Usage is ``python manage.py refreshfeeds``

    """

    def add_arguments(self, parser):
        parser.add_argument('--num-feeds', type=str)

    help = 'Refreshes the RSS feeds - 30 at a time by default. Use --num-feeds=all to refresh all feeds.'

    def handle(self, *args, **options):

        if options['num_feeds']:
            num_feeds = options['num_feeds']
        else:
            num_feeds = "30"

        if num_feeds == "all":
            num_feeds = 0
        else:
            num_feeds = int(num_feeds)

        self.stdout.write(self.style.SUCCESS('Starting'))

        update_feeds(max_feeds=num_feeds)

        self.stdout.write(self.style.SUCCESS('\nFinished'))
