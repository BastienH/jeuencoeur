from django.db import migrations

RENAMES = [
    {'old_slug': 'little-moments', 'new_name': 'Giggle Generators', 'new_slug': 'giggle-generators', 'new_icon': '😂', 'new_tagline': 'Tap for instant laughs!', 'game_module': 'giggle_generators'},
    {'old_slug': 'big-laughs', 'new_name': 'Choice Chaos', 'new_slug': 'choice-chaos', 'new_icon': '🤔', 'new_tagline': 'Silly debates for everyone!', 'game_module': 'choice_chaos'},
    {'old_slug': 'story-starters', 'new_name': 'Tale Twisters', 'new_slug': 'tale-twisters', 'new_icon': '📖', 'new_tagline': 'Collaborative story fun', 'game_module': 'tale_twisters'},
    {'old_slug': 'dare-devils', 'new_name': 'Mimic Mayhem', 'new_slug': 'mimic-mayhem', 'new_icon': '🔊', 'new_tagline': 'Imitate the sound!', 'game_module': 'mimic_mayhem'},
    {'old_slug': 'brain-teasers', 'new_name': 'Wild Roles', 'new_slug': 'wild-roles', 'new_icon': '🎭', 'new_tagline': 'Spin, act, and laugh!', 'game_module': 'wild_roles'},
    {'old_slug': 'feelings', 'new_name': 'Funny Face Factory', 'new_slug': 'funny-face-factory', 'new_icon': '📸', 'new_tagline': 'Make your silliest face!', 'game_module': 'funny_face_factory'},
    {'old_slug': 'movement', 'new_name': 'Lip-Sync Legends', 'new_slug': 'lip-sync-legends', 'new_icon': '🎤', 'new_tagline': 'Act out that sound!', 'game_module': 'lip_sync_legends'},
    {'old_slug': 'silly-sounds', 'new_name': 'Highway Hijinks', 'new_slug': 'highway-hijinks', 'new_icon': '🚗', 'new_tagline': 'Beat backseat boredom!', 'game_module': 'highway_hijinks'},
    {'old_slug': 'bedtime', 'new_name': 'Doodle Dash', 'new_slug': 'doodle-dash', 'new_icon': '🎨', 'new_tagline': 'Draw what you imagine!', 'game_module': 'doodle_dash'},
]


def rename_genres(apps, schema_editor):
    Genre = apps.get_model('games', 'Genre')
    for r in RENAMES:
        try:
            genre = Genre.objects.get(slug=r['old_slug'])
        except Genre.DoesNotExist:
            continue
        genre.name = r['new_name']
        genre.slug = r['new_slug']
        genre.icon = r['new_icon']
        genre.tagline = r['new_tagline']
        genre.game_module = r['game_module']
        genre.save()


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0003_add_game_module_to_genre'),
    ]

    operations = [
        migrations.RunPython(rename_genres, reverse_code=migrations.RunPython.noop),
    ]
