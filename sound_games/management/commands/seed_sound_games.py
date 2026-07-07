from django.core.management.base import BaseCommand, CommandError

from games.models import Genre
from sound_games.seed_data import (
    seed_micro_challenges,
    seed_wyr_questions,
    seed_sound_fx,
    seed_lip_sync_sounds,
)

GENRE_MODULES = ['giggle_generators', 'choice_chaos', 'mimic_mayhem', 'lip_sync_legends']


class Command(BaseCommand):
    help = 'Seed sound_games data'

    def handle(self, *args, **options):
        genres = Genre.objects.filter(game_module__in=GENRE_MODULES)
        if not genres.exists():
            self.stdout.write(self.style.WARNING('No matching genres found. Run games/seed first.'))
            return

        for genre in genres:
            self.stdout.write(f'\nSeeding data for {genre.name}...')
            seed_micro_challenges(genre, self.stdout)
            seed_wyr_questions(genre, self.stdout)
            seed_sound_fx(genre, self.stdout)
            seed_lip_sync_sounds(genre, self.stdout)

        self.stdout.write(self.style.SUCCESS('\nDone seeding sound_games!'))
