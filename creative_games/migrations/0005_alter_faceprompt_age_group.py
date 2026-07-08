from django.db import migrations, models

AGE_MAP = {
    'toddler': '3-6',
    'prek': '3-6',
    'elementary': '7-10',
}


def migrate_age_groups(apps, schema_editor):
    FacePrompt = apps.get_model('creative_games', 'FacePrompt')
    for old, new in AGE_MAP.items():
        FacePrompt.objects.filter(age_group=old).update(age_group=new)


def reverse_age_groups(apps, schema_editor):
    FacePrompt = apps.get_model('creative_games', 'FacePrompt')
    for new, old in AGE_MAP.items():
        FacePrompt.objects.filter(age_group=old).update(age_group=new)


class Migration(migrations.Migration):

    dependencies = [
        ('creative_games', '0004_faceprompt_age_group_faceprompt_category'),
    ]

    operations = [
        migrations.RunPython(migrate_age_groups, reverse_age_groups),
        migrations.AlterField(
            model_name='faceprompt',
            name='age_group',
            field=models.CharField(choices=[('all', 'All Ages'), ('3-6', '3-6'), ('7-10', '7-10'), ('11+', '11+')], db_index=True, default='all', max_length=20),
        ),
    ]
