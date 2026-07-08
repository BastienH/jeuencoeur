from django.db import migrations, models

AGE_MAP = {
    'toddler': '3-6',
    'prek': '3-6',
    'elementary': '7-10',
}


def migrate_age_groups(apps, schema_editor):
    MicroChallenge = apps.get_model('sound_games', 'MicroChallenge')
    for old, new in AGE_MAP.items():
        MicroChallenge.objects.filter(age_group=old).update(age_group=new)


def reverse_age_groups(apps, schema_editor):
    MicroChallenge = apps.get_model('sound_games', 'MicroChallenge')
    for new, old in AGE_MAP.items():
        MicroChallenge.objects.filter(age_group=old).update(age_group=new)


class Migration(migrations.Migration):

    dependencies = [
        ('sound_games', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_age_groups, reverse_age_groups),
        migrations.AlterModelOptions(
            name='wyrquestion',
            options={'ordering': ['?'], 'verbose_name': 'Choice', 'verbose_name_plural': 'Choices'},
        ),
        migrations.AlterField(
            model_name='microchallenge',
            name='age_group',
            field=models.CharField(choices=[('all', 'All Ages'), ('3-6', '3-6'), ('7-10', '7-10'), ('11+', '11+')], db_index=True, max_length=20),
        ),
    ]
