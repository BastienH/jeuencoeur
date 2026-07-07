import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import AnalyticsEvent, Genre

from .models import LipSyncSound, MicroChallenge, SoundFX, WYRQuestion


def giggle_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='giggle-generators')
    challenge = MicroChallenge.get_random(lang)
    return render(request, 'sound_games/giggle.html', {
        'genre': genre, 'challenge': challenge, 'lang': lang,
    })


def giggle_next(request, lang):
    activate(lang)
    age_group = request.GET.get('age_group')
    energy_level = request.GET.get('energy_level')
    challenge = MicroChallenge.get_random(lang, age_group, energy_level)
    return render(request, 'sound_games/partials/giggle_challenge.html', {
        'challenge': challenge, 'lang': lang,
    })


def choice_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='choice-chaos')
    question = WYRQuestion.get_random(lang)
    return render(request, 'sound_games/choice.html', {
        'genre': genre, 'question': question, 'lang': lang,
    })


def choice_reroll(request, lang):
    activate(lang)
    category = request.GET.get('category')
    question = WYRQuestion.get_random(lang, category)
    return render(request, 'sound_games/partials/choice_question.html', {
        'question': question, 'lang': lang,
    })


@require_POST
def choice_vote(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    question_id = data.get('question_id')
    vote = data.get('vote')
    AnalyticsEvent.objects.create(
        event_type='wyr_vote',
        genre=get_object_or_404(Genre, slug='choice-chaos'),
        metadata={'question_id': question_id, 'vote': vote},
        language=lang,
    )
    return JsonResponse({'status': 'ok', 'vote': vote})


def mimic_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='mimic-mayhem')
    sound = SoundFX.get_random()
    return render(request, 'sound_games/mimic.html', {
        'genre': genre, 'sound': sound, 'lang': lang,
    })


def mimic_next(request, lang):
    sound = SoundFX.get_random()
    return render(request, 'sound_games/partials/mimic_sound.html', {
        'sound': sound, 'lang': lang,
    })


def lip_sync_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='lip-sync-legends')
    sound = LipSyncSound.get_random()
    if sound:
        sound.display_description = sound.get_description(lang)
    return render(request, 'sound_games/lip_sync.html', {
        'genre': genre, 'sound': sound, 'lang': lang,
    })


def lip_sync_next(request, lang):
    sound = LipSyncSound.get_random()
    if sound:
        sound.display_description = sound.get_description(lang)
    return render(request, 'sound_games/partials/lip_sync_sound.html', {
        'sound': sound, 'lang': lang,
    })
