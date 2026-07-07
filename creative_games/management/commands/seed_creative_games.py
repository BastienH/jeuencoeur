from django.core.management.base import BaseCommand

from games.models import Genre
from creative_games.seed_data import seed_story_endings, seed_story_twists, seed_face_prompts, seed_doodle_data

GENRE_MODULES = ['tale_twisters', 'funny_face_factory', 'doodle_dash']


class Command(BaseCommand):
    help = 'Seed creative_games data'

    def handle(self, *args, **options):
        genres = Genre.objects.filter(game_module__in=GENRE_MODULES)
        if not genres.exists():
            self.stdout.write(self.style.WARNING('No matching genres found. Run games/seed first.'))
            return

        for genre in genres:
            self.stdout.write(f'\nSeeding data for {genre.name}...')
            if genre.game_module == 'tale_twisters':
                seed_story_twists(genre, self.stdout)
                seed_story_endings(genre, self.stdout)
            elif genre.game_module == 'funny_face_factory':
                seed_face_prompts(genre, self.stdout)
            elif genre.game_module == 'doodle_dash':
                seed_doodle_data(self.stdout)

        self.stdout.write(self.style.SUCCESS('\nDone seeding creative_games!'))
