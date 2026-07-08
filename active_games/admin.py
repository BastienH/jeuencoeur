from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (CarGame, RoleActivity, RoleCharacter, RoleSetting,
                     TripSession)
from games.resources import (CarGameResource, RoleActivityResource,
                             RoleCharacterResource, RoleSettingResource)


@admin.register(RoleCharacter)
class RoleCharacterAdmin(ImportExportModelAdmin):
    resource_class = RoleCharacterResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(RoleSetting)
class RoleSettingAdmin(ImportExportModelAdmin):
    resource_class = RoleSettingResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(RoleActivity)
class RoleActivityAdmin(ImportExportModelAdmin):
    resource_class = RoleActivityResource
    list_display = ('id', 'text_en_preview')
    search_fields = ('text_en',)

    def text_en_preview(self, obj):
        return obj.text_en[:60]


@admin.register(CarGame)
class CarGameAdmin(ImportExportModelAdmin):
    resource_class = CarGameResource
    list_display = ('name_en', 'min_age', 'genre')
    list_filter = ('min_age', 'genre')
    search_fields = ('name_en', 'instructions_en')
    autocomplete_fields = ['genre']


@admin.register(TripSession)
class TripSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'progress_pct', 'start_time', 'end_time')
    list_filter = ('active',)
    raw_id_fields = ('user',)
