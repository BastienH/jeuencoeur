from django.db import migrations, models

AGE_MAP = {
    'toddler': '3-6',
    'prek': '3-6',
    'elementary': '7-10',
}


def migrate_age_groups(apps, schema_editor):
    CarGame = apps.get_model('active_games', 'CarGame')
    for old, new in AGE_MAP.items():
        CarGame.objects.filter(min_age=old).update(min_age=new)


def reverse_age_groups(apps, schema_editor):
    CarGame = apps.get_model('active_games', 'CarGame')
    for new, old in AGE_MAP.items():
        CarGame.objects.filter(min_age=old).update(min_age=new)


class Migration(migrations.Migration):

    dependencies = [
        ('active_games', '0002_tripsession_games_shown'),
    ]

    operations = [
        migrations.RunPython(migrate_age_groups, reverse_age_groups),
        migrations.AlterField(
            model_name='cargame',
            name='min_age',
            field=models.CharField(choices=[('all', 'All Ages'), ('3-6', '3-6'), ('7-10', '7-10'), ('11+', '11+')], default='all', max_length=20),
        ),
    ]
