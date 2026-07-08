from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (DoodleAccessory, DoodleDrawing, DoodleEmotion,
                     DoodleSubject, FacePrompt, StoryEnding, StorySession, StoryTwist)
from games.resources import (DoodleAccessoryResource, DoodleEmotionResource,
                             DoodleSubjectResource, FacePromptResource,
                             StoryEndingResource, StoryTwistResource)


@admin.register(StoryTwist)
class StoryTwistAdmin(ImportExportModelAdmin):
    resource_class = StoryTwistResource
    list_display = ('id', 'text_en_preview', 'genre')
    list_filter = ('genre',)
    search_fields = ('text_en',)
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(StoryEnding)
class StoryEndingAdmin(ImportExportModelAdmin):
    resource_class = StoryEndingResource
    list_display = ('id', 'text_en_preview', 'genre')
    list_filter = ('genre',)
    search_fields = ('text_en',)
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(StorySession)
class StorySessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'duration_seconds', 'created_at')
    list_filter = ('language',)
    search_fields = ('title', 'content')
    raw_id_fields = ('user',)


@admin.register(FacePrompt)
class FacePromptAdmin(ImportExportModelAdmin):
    resource_class = FacePromptResource
    list_display = ('id', 'text_en_preview', 'genre')
    list_filter = ('genre',)
    search_fields = ('text_en',)
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleSubject)
class DoodleSubjectAdmin(ImportExportModelAdmin):
    resource_class = DoodleSubjectResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleEmotion)
class DoodleEmotionAdmin(ImportExportModelAdmin):
    resource_class = DoodleEmotionResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleAccessory)
class DoodleAccessoryAdmin(ImportExportModelAdmin):
    resource_class = DoodleAccessoryResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleDrawing)
class DoodleDrawingAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt_subject', 'user', 'created_at')
    raw_id_fields = ('user',)
