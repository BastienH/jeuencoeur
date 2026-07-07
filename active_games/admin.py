from django.contrib import admin

from .models import (CarGame, RoleActivity, RoleCharacter, RoleSetting,
                     TripSession)


@admin.register(RoleCharacter)
class RoleCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(RoleSetting)
class RoleSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(RoleActivity)
class RoleActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(CarGame)
class CarGameAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'min_age', 'genre')
    list_filter = ('min_age', 'genre')
    search_fields = ('name_en', 'instructions_en')
    autocomplete_fields = ['genre']


@admin.register(TripSession)
class TripSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'progress_pct', 'start_time', 'end_time')
    list_filter = ('active',)
    raw_id_fields = ('user',)
