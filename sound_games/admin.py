from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import LipSyncSound, MicroChallenge, SoundFX, WYRQuestion
from games.resources import (LipSyncSoundResource, MicroChallengeResource,
                             SoundFXResource, WYRQuestionResource)


@admin.register(MicroChallenge)
class MicroChallengeAdmin(ImportExportModelAdmin):
    resource_class = MicroChallengeResource
    list_display = ('text_en_preview', 'age_group', 'energy_level', 'duration_seconds', 'genre')
    list_filter = ('age_group', 'energy_level', 'genre')
    search_fields = ('text_en', 'text_fr', 'text_es')
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(WYRQuestion)
class WYRQuestionAdmin(ImportExportModelAdmin):
    resource_class = WYRQuestionResource
    list_display = ('id', 'category', 'genre', 'option_a_en_preview')
    list_filter = ('category', 'genre')
    search_fields = ('option_a_en', 'option_b_en')
    autocomplete_fields = ['genre']
    fields = (
        'genre',
        'category',
        ('option_a_en', 'option_b_en'),
        ('option_a_fr', 'option_b_fr'),
        ('option_a_es', 'option_b_es'),
    )

    def option_a_en_preview(self, obj):
        return obj.option_a_en[:60]


@admin.register(SoundFX)
class SoundFXAdmin(ImportExportModelAdmin):
    resource_class = SoundFXResource
    list_display = ('name', 'category', 'genre')
    list_filter = ('category', 'genre')
    search_fields = ('name',)
    autocomplete_fields = ['genre']


@admin.register(LipSyncSound)
class LipSyncSoundAdmin(ImportExportModelAdmin):
    resource_class = LipSyncSoundResource
    list_display = ('name', 'genre')
    list_filter = ('genre',)
    search_fields = ('name', 'description_en')
    autocomplete_fields = ['genre']
