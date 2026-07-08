import random

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class StoryTwist(models.Model):
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='story_twists')
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    @staticmethod
    def get_random(lang):
        count = StoryTwist.objects.count()
        if count == 0:
            return None
        t = StoryTwist.objects.all()[random.randint(0, count - 1)]
        t.display_text = t.get_text(lang)
        return t


class StorySession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='stories/', null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    language = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Story #{self.id}"


CATEGORIES = [
    ('silly', _('Silly')),
    ('happy', _('Happy')),
    ('sad', _('Sad')),
    ('angry', _('Angry')),
    ('surprised', _('Surprised')),
    ('scared', _('Scared')),
    ('sleepy', _('Sleepy')),
    ('brave', _('Brave')),
    ('grumpy', _('Grumpy')),
    ('funny', _('Funny')),
]

AGE_GROUPS = [
    ('toddler', _('Toddler')),
    ('prek', _('Pre-K')),
    ('elementary', _('Elementary')),
    ('all', _('All Ages')),
]


class FacePrompt(models.Model):
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='face_prompts')
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS, default='all', db_index=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='silly', db_index=True)
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    @staticmethod
    def get_random(lang, age_group=None, category=None):
        qs = FacePrompt.objects.all()
        if age_group and age_group != 'all':
            qs = qs.filter(age_group=age_group)
        if category:
            qs = qs.filter(category=category)
        if not qs.exists():
            qs = FacePrompt.objects.all()
        count = qs.count()
        if count == 0:
            return None
        p = qs[random.randint(0, count - 1)]
        p.display_text = p.get_text(lang)
        return p


class StoryEnding(models.Model):
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='story_endings')
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['?']

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    @staticmethod
    def get_random(lang):
        count = StoryEnding.objects.count()
        if count == 0:
            return None
        e = StoryEnding.objects.all()[random.randint(0, count - 1)]
        e.display_text = e.get_text(lang)
        return e


class DoodleSubject(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class DoodleEmotion(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class DoodleAccessory(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:60]

    def get_text(self, lang):
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en


class DoodleDrawing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    prompt_subject = models.CharField(max_length=200, blank=True)
    prompt_emotion = models.CharField(max_length=200, blank=True)
    prompt_accessory = models.CharField(max_length=200, blank=True)
    image = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Doodle #{self.id}"
