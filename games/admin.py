from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import AnalyticsEvent, Favorite, Genre, Prompt, SoundEffect, StorySeed, UserProfile
from .resources import (GenreResource, PromptResource, SoundEffectResource,
                        StorySeedResource)


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_class = GenreResource
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Prompt)
class PromptAdmin(ImportExportModelAdmin):
    resource_class = PromptResource
    list_display = ('id', 'genre', 'category', 'text_en_preview')
    list_filter = ('genre', 'category')
    search_fields = ('text_en', 'text_fr', 'text_es')
    autocomplete_fields = ['genre']
    list_select_related = ('genre',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]
    text_en_preview.short_description = 'English preview'

    def save_model(self, request, obj, form, change):
        if not obj.text_en or not obj.text_fr or not obj.text_es:
            from django.contrib import messages
            missing = []
            if not obj.text_en:
                missing.append('English')
            if not obj.text_fr:
                missing.append('French')
            if not obj.text_es:
                missing.append('Spanish')
            messages.set_level(request, messages.ERROR)
            raise ValueError(
                f"All translations are required. Missing: {', '.join(missing)}"
            )
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ('text_en', 'text_fr', 'text_es'):
            form.base_fields[field].required = True
        return form


@admin.register(StorySeed)
class StorySeedAdmin(ImportExportModelAdmin):
    resource_class = StorySeedResource
    list_display = ('id', 'genre', 'category', 'text_en_preview')
    list_filter = ('genre', 'category')
    search_fields = ('text_en', 'text_fr', 'text_es')
    autocomplete_fields = ['genre']
    list_select_related = ('genre',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]
    text_en_preview.short_description = 'English preview'

    def save_model(self, request, obj, form, change):
        if not obj.text_en or not obj.text_fr or not obj.text_es:
            from django.contrib import messages
            missing = []
            if not obj.text_en:
                missing.append('English')
            if not obj.text_fr:
                missing.append('French')
            if not obj.text_es:
                missing.append('Spanish')
            messages.set_level(request, messages.ERROR)
            raise ValueError(
                f"All translations are required. Missing: {', '.join(missing)}"
            )
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ('text_en', 'text_fr', 'text_es'):
            form.base_fields[field].required = True
        return form


@admin.register(SoundEffect)
class SoundEffectAdmin(ImportExportModelAdmin):
    resource_class = SoundEffectResource
    list_display = ('name', 'audio_file_display', 'genre_list')
    list_filter = ('genres',)
    search_fields = ('name', 'description_en')
    filter_horizontal = ('genres',)

    def audio_file_display(self, obj):
        return obj.audio_file.name if obj.audio_file else '-'
    audio_file_display.short_description = 'Audio file'

    def genre_list(self, obj):
        return ', '.join(g.name for g in obj.genres.all())
    genre_list.short_description = 'Genres'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_tester', 'created_at')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)

    def is_tester(self, obj):
        return obj.settings.get('is_tester', False)
    is_tester.boolean = True
    is_tester.short_description = 'Tester'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt', 'created_at')
    list_select_related = ('user', 'prompt__genre')
    raw_id_fields = ('user', 'prompt')


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'event_type', 'genre', 'language', 'user')
    list_filter = ('event_type', 'created_at', 'language')
    search_fields = ('session_key',)
    raw_id_fields = ('user', 'genre', 'prompt')
    readonly_fields = ('event_type', 'genre', 'prompt', 'user', 'session_key', 'language', 'metadata', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
