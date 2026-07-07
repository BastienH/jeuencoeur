from django.core.management.base import BaseCommand

from games.models import Genre
from active_games.seed_data import seed_role_data, seed_car_games

GENRE_MODULES = ['wild_roles', 'highway_hijinks']


class Command(BaseCommand):
    help = 'Seed active_games data'

    def handle(self, *args, **options):
        genres = Genre.objects.filter(game_module__in=GENRE_MODULES)
        if not genres.exists():
            self.stdout.write(self.style.WARNING('No matching genres found. Run games/seed first.'))
            return

        for genre in genres:
            self.stdout.write(f'\nSeeding data for {genre.name}...')
            if genre.game_module == 'wild_roles':
                seed_role_data(genre, self.stdout)
            elif genre.game_module == 'highway_hijinks':
                seed_car_games(genre, self.stdout)

        self.stdout.write(self.style.SUCCESS('\nDone seeding active_games!'))
