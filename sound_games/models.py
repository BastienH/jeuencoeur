import random

from django.db import models
from django.utils.translation import gettext_lazy as _


class MicroChallenge(models.Model):
    AGE_GROUPS = [
        ('all', _('All Ages')),
        ('3-6', _('3-6')),
        ('7-10', _('7-10')),
        ('11+', _('11+')),
    ]
    ENERGY_LEVELS = [
        ('calm', _('Calm')),
        ('wild', _('Wild')),
    ]

    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='micro_challenges')
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS, db_index=True)
    energy_level = models.CharField(max_length=20, choices=ENERGY_LEVELS, db_index=True)
    duration_seconds = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']
        indexes = [
            models.Index(fields=['age_group', 'energy_level']),
        ]

    def __str__(self):
        return f"[{self.age_group}/{self.energy_level}] {self.text_en[:50]}..."

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    @staticmethod
    def get_random(lang, age_group=None, energy_level=None):
        qs = MicroChallenge.objects.all()
        if age_group:
            qs = qs.filter(age_group=age_group)
        if energy_level:
            qs = qs.filter(energy_level=energy_level)
        count = qs.count()
        if count == 0:
            return None
        challenge = qs[random.randint(0, count - 1)]
        challenge.display_text = challenge.get_text(lang)
        return challenge


class WYRQuestion(models.Model):
    AGE_GROUPS = [
        ('all', _('All Ages')),
        ('3-6', _('3-6')),
        ('7-10', _('7-10')),
        ('11+', _('11+')),
    ]
    CATEGORIES = [
        ('silly', _('Silly')),
        ('deep', _('Deep')),
        ('food', _('Food')),
        ('animals', _('Animals')),
        ('superpower', _('Superpower')),
        ('gross', _('Gross')),
        ('adventure', _('Adventure')),
        ('school', _('School')),
    ]

    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='wyr_questions')
    category = models.CharField(max_length=20, choices=CATEGORIES, db_index=True)
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS, default='all', db_index=True)
    option_a_en = models.TextField()
    option_a_fr = models.TextField()
    option_a_es = models.TextField()
    option_b_en = models.TextField()
    option_b_fr = models.TextField()
    option_b_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        ordering = ['?']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['age_group']),
        ]

    def __str__(self):
        return f"[{self.category}/{self.age_group}] {self.option_a_en[:40]}... vs {self.option_b_en[:40]}..."

    def get_option_a(self, lang):
        return getattr(self, f'option_a_{lang}', self.option_a_en) or self.option_a_en

    def get_option_b(self, lang):
        return getattr(self, f'option_b_{lang}', self.option_b_en) or self.option_b_en

    @staticmethod
    def get_random(lang, category=None, age_group=None):
        qs = WYRQuestion.objects.all()
        if category:
            qs = qs.filter(category=category)
        if age_group and age_group != 'all':
            qs = qs.filter(age_group=age_group)
        count = qs.count()
        if count == 0:
            return None
        q = qs[random.randint(0, count - 1)]
        q.display_a = q.get_option_a(lang)
        q.display_b = q.get_option_b(lang)
        return q


class SoundFX(models.Model):
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='sound_fx')
    name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='sfx/')
    category = models.CharField(max_length=50, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @staticmethod
    def get_random():
        count = SoundFX.objects.count()
        if count == 0:
            return None
        return SoundFX.objects.all()[random.randint(0, count - 1)]


class LipSyncSound(models.Model):
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='lip_sync_sounds')
    name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='lipsync/')
    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description_es = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_description(self, lang):
        return getattr(self, f'description_{lang}', self.description_en) or self.description_en

    @staticmethod
    def get_random():
        count = LipSyncSound.objects.count()
        if count == 0:
            return None
        return LipSyncSound.objects.all()[random.randint(0, count - 1)]
