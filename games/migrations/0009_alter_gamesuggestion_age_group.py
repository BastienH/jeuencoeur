from django.db import migrations, models

AGE_MAP = {
    'toddler': '3-6',
    'prek': '3-6',
    'elementary': '7-10',
}


def migrate_age_groups(apps, schema_editor):
    GameSuggestion = apps.get_model('games', 'GameSuggestion')
    for old, new in AGE_MAP.items():
        GameSuggestion.objects.filter(age_group=old).update(age_group=new)


def reverse_age_groups(apps, schema_editor):
    GameSuggestion = apps.get_model('games', 'GameSuggestion')
    for new, old in AGE_MAP.items():
        GameSuggestion.objects.filter(age_group=old).update(age_group=new)


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_contactmessage_gamesuggestion'),
    ]

    operations = [
        migrations.RunPython(migrate_age_groups, reverse_age_groups),
        migrations.AlterField(
            model_name='gamesuggestion',
            name='age_group',
            field=models.CharField(blank=True, choices=[('', '---------'), ('all', 'All Ages'), ('3-6', '3-6'), ('7-10', '7-10'), ('11+', '11+')], help_text='For MicroChallenge', max_length=20),
        ),
    ]
