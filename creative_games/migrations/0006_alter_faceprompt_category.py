from django.db import migrations, models

CAT_MAP = {
    'happy': 'emotions',
    'sad': 'emotions',
    'angry': 'emotions',
    'surprised': 'emotions',
    'scared': 'emotions',
    'grumpy': 'emotions',
    'sleepy': 'sensations',
    'brave': 'characters',
    'funny': 'absurd',
}


def migrate_categories(apps, schema_editor):
    FacePrompt = apps.get_model('creative_games', 'FacePrompt')
    for old, new in CAT_MAP.items():
        FacePrompt.objects.filter(category=old).update(category=new)


def reverse_categories(apps, schema_editor):
    FacePrompt = apps.get_model('creative_games', 'FacePrompt')
    for new, old in CAT_MAP.items():
        FacePrompt.objects.filter(category=old).update(category=new)


class Migration(migrations.Migration):

    dependencies = [
        ('creative_games', '0005_alter_faceprompt_age_group'),
    ]

    operations = [
        migrations.RunPython(migrate_categories, reverse_categories),
        migrations.AlterField(
            model_name='faceprompt',
            name='category',
            field=models.CharField(choices=[('silly', 'Silly'), ('emotions', 'Emotions'), ('animals', 'Animals'), ('sensations', 'Sensations'), ('technical', 'Technical'), ('situations', 'Situations'), ('absurd', 'Absurd'), ('characters', 'Characters')], db_index=True, default='silly', max_length=20),
        ),
    ]
