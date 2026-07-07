import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class PromptManager(models.Manager):
    def get_random(self, genre, lang):
        qs = self.get_queryset().filter(genre=genre)
        count = qs.count()
        if count == 0:
            return None
        random_index = random.randint(0, count - 1)
        prompt = qs[random_index]
        prompt.display_text = prompt.get_text(lang)
        return prompt


class Genre(models.Model):
    name = models.CharField(max_length=50)
    name_fr = models.CharField(max_length=50, default='')
    name_es = models.CharField(max_length=50, default='')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10)
    tagline = models.CharField(max_length=100, blank=True)
    tagline_fr = models.CharField(max_length=100, blank=True, default='')
    tagline_es = models.CharField(max_length=100, blank=True, default='')
    game_module = models.CharField(max_length=50, blank=True, db_index=True,
                                   help_text='e.g. giggle_generators, choice_chaos — blank uses generic detail view')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_name(self, lang):
        return getattr(self, f'name_{lang}', self.name) or self.name

    def get_tagline(self, lang):
        return getattr(self, f'tagline_{lang}', self.tagline) or self.tagline


class Prompt(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='prompts', db_index=True)
    category = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()

    objects = PromptManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.genre.name}: {self.text_en[:50]}..."

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class StorySeedManager(models.Manager):
    def get_random(self, genre, lang):
        qs = self.get_queryset().filter(genre=genre)
        count = qs.count()
        if count == 0:
            return None
        random_index = random.randint(0, count - 1)
        seed = qs[random_index]
        seed.display_text = seed.get_text(lang)
        return seed


class StorySeed(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='story_seeds', db_index=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StorySeedManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.genre.name}: {self.text_en[:50]}..."

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class SoundEffect(models.Model):
    name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='sounds/')
    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_es = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name='sound_effects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'prompt')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ♥ {self.prompt}"


class AnalyticsEvent(models.Model):
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('prompt_view', 'Prompt View'),
        ('prompt_reroll', 'Prompt Reroll'),
        ('genre_enter', 'Genre Enter'),
        ('genre_abandon', 'Genre Abandon'),
        ('favorite_add', 'Favorite Added'),
        ('favorite_remove', 'Favorite Removed'),
        ('language_switch', 'Language Switch'),
        ('wyr_vote', 'WYR Vote'),
        ('wild_reaction', 'Wild Role Reaction'),
        ('giggle_reroll', 'Giggle Reroll'),
        ('mimic_play', 'Mimic Sound Played'),
        ('lipsync_play', 'Lip Sync Sound Played'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    language = models.CharField(max_length=10, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['genre', 'event_type']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.event_type}"
