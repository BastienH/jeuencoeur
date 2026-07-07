from django.contrib import admin

from .models import (DoodleAccessory, DoodleDrawing, DoodleEmotion,
                     DoodleSubject, FacePrompt, StoryEnding, StorySession, StoryTwist)


@admin.register(StoryTwist)
class StoryTwistAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview', 'genre')
    list_filter = ('genre',)
    search_fields = ('text_en',)
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(StoryEnding)
class StoryEndingAdmin(admin.ModelAdmin):
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
class FacePromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview', 'genre')
    list_filter = ('genre',)
    search_fields = ('text_en',)
    autocomplete_fields = ['genre']

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleSubject)
class DoodleSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleEmotion)
class DoodleEmotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleAccessory)
class DoodleAccessoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(DoodleDrawing)
class DoodleDrawingAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt_subject', 'user', 'created_at')
    raw_id_fields = ('user',)
