from django.contrib import admin

from .models import LipSyncSound, MicroChallenge, SoundFX, WYRQuestion


@admin.register(MicroChallenge)
class MicroChallengeAdmin(admin.ModelAdmin):
    list_display = ('text_en_preview', 'age_group', 'energy_level', 'duration_seconds', 'genre')
    list_filter = ('age_group', 'energy_level', 'genre')
    search_fields = ('text_en', 'text_fr', 'text_es')
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(WYRQuestion)
class WYRQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'genre', 'option_a_en_preview')
    list_filter = ('category', 'genre')
    search_fields = ('option_a_en', 'option_b_en')
    autocomplete_fields = ['genre']

    def option_a_en_preview(self, obj):
        return obj.option_a_en[:60]


@admin.register(SoundFX)
class SoundFXAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'genre')
    list_filter = ('category', 'genre')
    search_fields = ('name',)
    autocomplete_fields = ['genre']


@admin.register(LipSyncSound)
class LipSyncSoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    list_filter = ('genre',)
    search_fields = ('name', 'description_en')
    autocomplete_fields = ['genre']
