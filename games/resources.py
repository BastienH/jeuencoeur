from import_export import resources, fields, widgets

from active_games.models import CarGame, RoleActivity, RoleCharacter, RoleSetting
from creative_games.models import (DoodleAccessory, DoodleEmotion, DoodleSubject,
                                    FacePrompt, StoryEnding, StoryTwist)
from games.models import Genre, Prompt, SoundEffect, StorySeed
from sound_games.models import (LipSyncSound, MicroChallenge, SoundFX,
                                 WYRQuestion)


class GenreForeignKeyWidget(widgets.ForeignKeyWidget):
    def __init__(self):
        super().__init__(Genre, field='name')


class _BaseResource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        report_skipped = True
        import_id_fields = []
        exclude = ('id', 'created_at', 'updated_at')


class GenreResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = Genre
        fields = ('name', 'name_fr', 'name_es', 'slug', 'icon',
                  'tagline', 'tagline_fr', 'tagline_es', 'order', 'is_active')


class PromptResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = Prompt
        fields = ('genre', 'category', 'text_en', 'text_fr', 'text_es')


class StorySeedResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = StorySeed
        fields = ('genre', 'category', 'text_en', 'text_fr', 'text_es')


class SoundEffectResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = SoundEffect
        fields = ('name', 'description_en', 'description_fr', 'description_es', 'genres', 'audio_file')


class MicroChallengeResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = MicroChallenge
        fields = ('genre', 'age_group', 'energy_level', 'duration_seconds',
                  'text_en', 'text_fr', 'text_es')


class WYRQuestionResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = WYRQuestion
        fields = ('genre', 'category',
                  'option_a_en', 'option_b_en',
                  'option_a_fr', 'option_b_fr',
                  'option_a_es', 'option_b_es')


class SoundFXResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = SoundFX
        fields = ('genre', 'name', 'category', 'audio_file')


class LipSyncSoundResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = LipSyncSound
        fields = ('genre', 'name', 'description_en', 'description_fr', 'description_es', 'audio_file')


class StoryTwistResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = StoryTwist
        fields = ('genre', 'text_en', 'text_fr', 'text_es')


class StoryEndingResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = StoryEnding
        fields = ('genre', 'text_en', 'text_fr', 'text_es')


class FacePromptResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = FacePrompt
        fields = ('genre', 'text_en', 'text_fr', 'text_es')


class DoodleSubjectResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = DoodleSubject
        fields = ('text_en', 'text_fr', 'text_es')


class DoodleEmotionResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = DoodleEmotion
        fields = ('text_en', 'text_fr', 'text_es')


class DoodleAccessoryResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = DoodleAccessory
        fields = ('text_en', 'text_fr', 'text_es')


class RoleCharacterResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = RoleCharacter
        fields = ('text_en', 'text_fr', 'text_es')


class RoleSettingResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = RoleSetting
        fields = ('text_en', 'text_fr', 'text_es')


class RoleActivityResource(_BaseResource):
    class Meta(_BaseResource.Meta):
        model = RoleActivity
        fields = ('text_en', 'text_fr', 'text_es')


class CarGameResource(_BaseResource):
    genre = fields.Field(column_name='genre', attribute='genre', widget=GenreForeignKeyWidget())

    class Meta(_BaseResource.Meta):
        model = CarGame
        fields = ('genre', 'min_age',
                  'name_en', 'name_fr', 'name_es',
                  'instructions_en', 'instructions_fr', 'instructions_es')
