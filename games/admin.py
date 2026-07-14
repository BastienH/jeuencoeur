from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (AnalyticsEvent, ContactMessage, Favorite, GameSuggestion,
                     Genre, Prompt, StorySeed, UserProfile)
from .resources import GenreResource, PromptResource, StorySeedResource


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message_preview', 'dealt_with', 'created_at')
    list_filter = ('dealt_with',)
    search_fields = ('email', 'message')
    actions = ['mark_dealt_with']
    date_hierarchy = 'created_at'

    def message_preview(self, obj):
        return obj.message[:80]
    message_preview.short_description = 'Message'

    @admin.action(description='Mark selected as dealt with')
    def mark_dealt_with(self, request, queryset):
        queryset.update(dealt_with=True)


@admin.register(GameSuggestion)
class GameSuggestionAdmin(admin.ModelAdmin):
    list_display = ('genre', 'suggestion_preview', 'email', 'status_colored', 'target_model', 'created_at')
    list_filter = ('status', 'genre', 'target_model')
    search_fields = ('suggestion_text', 'email', 'text_en', 'text_fr', 'text_es')
    autocomplete_fields = ['genre']
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('genre', 'email', 'suggestion_text', 'target_model'),
        }),
        ('Translations (fill when accepting)', {
            'fields': ('text_en', 'text_fr', 'text_es'),
            'classes': ('wide',),
        }),
        ('Extra fields', {
            'fields': ('category', ('age_group', 'energy_level'), 'duration_seconds'),
            'classes': ('wide',),
            'description': 'For Prompt/Story Seed: category. For MicroChallenge: age_group, energy_level, duration_seconds.',
        }),
        ('Review', {
            'fields': ('status', 'admin_notes'),
        }),
    )

    def suggestion_preview(self, obj):
        return obj.suggestion_text[:60]
    suggestion_preview.short_description = 'Suggestion'

    def status_colored(self, obj):
        colors = {'pending': 'orange', 'accepted': 'green', 'denied': 'red'}
        c = colors.get(obj.status, 'gray')
        from django.utils.html import format_html
        return format_html('<span style="color:{};font-weight:600">{}</span>', c, obj.get_status_display())
    status_colored.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if obj.pk:
            old = self.model.objects.get(pk=obj.pk)
            was_accepted = old.status == 'accepted'
        else:
            was_accepted = False
        super().save_model(request, obj, form, change)
        if obj.status == 'accepted' and not was_accepted and not obj.prompt_created:
            _create_target_model_record(obj)
            obj.prompt_created = True
            obj.save(update_fields=['prompt_created'])


def _create_target_model_record(suggestion):
    from creative_games.models import FacePrompt, StoryEnding, StoryTwist
    from sound_games.models import MicroChallenge
    from .models import Prompt, StorySeed

    text_en = suggestion.text_en or suggestion.suggestion_text
    text_fr = suggestion.text_fr or text_en
    text_es = suggestion.text_es or text_en

    creators = {
        'prompt': lambda: Prompt.objects.create(
            genre=suggestion.genre, category=suggestion.category or '',
            text_en=text_en, text_fr=text_fr, text_es=text_es,
        ),
        'story_seed': lambda: StorySeed.objects.create(
            genre=suggestion.genre, category=suggestion.category or '',
            text_en=text_en, text_fr=text_fr, text_es=text_es,
        ),
        'story_twist': lambda: StoryTwist.objects.create(
            genre=suggestion.genre,
            text_en=text_en, text_fr=text_fr, text_es=text_es,
        ),
        'story_ending': lambda: StoryEnding.objects.create(
            genre=suggestion.genre,
            text_en=text_en, text_fr=text_fr, text_es=text_es,
        ),
        'face_prompt': lambda: FacePrompt.objects.create(
            genre=suggestion.genre,
            text_en=text_en, text_fr=text_fr, text_es=text_es,
        ),
        'micro_challenge': lambda: MicroChallenge.objects.create(
            genre=suggestion.genre,
            text_en=text_en, text_fr=text_fr, text_es=text_es,
            age_group=suggestion.age_group or '3-6',
            energy_level=suggestion.energy_level or 'calm',
            duration_seconds=suggestion.duration_seconds or 20,
        ),
    }
    creator = creators.get(suggestion.target_model)
    if creator:
        creator()
