import random

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleCharacter(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class RoleSetting(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class RoleActivity(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class CarGame(models.Model):
    AGE_GROUPS = [
        ('all', _('All Ages')),
        ('3-6', _('3-6')),
        ('7-10', _('7-10')),
        ('11+', _('11+')),
    ]

    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='car_games')
    name_en = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100, blank=True)
    name_es = models.CharField(max_length=100, blank=True)
    instructions_en = models.TextField()
    instructions_fr = models.TextField(blank=True)
    instructions_es = models.TextField(blank=True)
    min_age = models.CharField(max_length=20, choices=AGE_GROUPS, default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return self.name_en

    def get_name(self, lang):
        return getattr(self, f'name_{lang}', self.name_en) or self.name_en

    def get_instructions(self, lang):
        return getattr(self, f'instructions_{lang}', self.instructions_en) or self.instructions_en


class TripSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    start_lat = models.FloatField(null=True, blank=True)
    start_lon = models.FloatField(null=True, blank=True)
    end_lat = models.FloatField(null=True, blank=True)
    end_lon = models.FloatField(null=True, blank=True)
    total_distance_km = models.FloatField(default=0)
    progress_pct = models.IntegerField(default=0)
    games_shown = models.JSONField(default=list, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    language = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Trip #{self.id} ({self.progress_pct}%)"
