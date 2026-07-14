import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import AnalyticsEvent, Genre
from games.utils import get_shuffled_item, require_active_game

from .models import LipSyncSound, MicroChallenge, SoundFX, WYRQuestion


@require_active_game('giggle-generators')
def giggle_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='giggle-generators')
    challenge = get_shuffled_item(
        request, 'deck_giggle',
        MicroChallenge.objects.all(),
    )
    if challenge:
        challenge.display_text = challenge.get_text(lang)
    return render(request, 'sound_games/giggle.html', {
        'genre': genre, 'challenge': challenge, 'lang': lang,
    })


@require_active_game('giggle-generators')
def giggle_next(request, lang):
    activate(lang)
    age_group = request.GET.get('age_group')
    energy_level = request.GET.get('energy_level')
    filters = {}
    if age_group:
        filters['age_group'] = age_group
    if energy_level:
        filters['energy_level'] = energy_level
    qs = MicroChallenge.objects.all()
    if age_group:
        qs = qs.filter(age_group=age_group)
    if energy_level:
        qs = qs.filter(energy_level=energy_level)
    challenge = get_shuffled_item(
        request, 'deck_giggle', qs,
        filters=filters or None, advance=True,
    )
    if challenge:
        challenge.display_text = challenge.get_text(lang)
    return render(request, 'sound_games/partials/giggle_challenge.html', {
        'challenge': challenge, 'lang': lang,
    })


@require_active_game('choice-chaos')
def choice_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='choice-chaos')
    question = get_shuffled_item(
        request, 'deck_choice',
        WYRQuestion.objects.all(),
    )
    if question:
        question.display_a = question.get_option_a(lang)
        question.display_b = question.get_option_b(lang)
    return render(request, 'sound_games/choice.html', {
        'genre': genre, 'question': question, 'lang': lang,
    })


@require_active_game('choice-chaos')
def choice_reroll(request, lang):
    activate(lang)
    category = request.GET.get('category')
    filters = {'category': category} if category else None
    qs = WYRQuestion.objects.all()
    if category:
        qs = qs.filter(category=category)
    question = get_shuffled_item(
        request, 'deck_choice', qs,
        filters=filters, advance=True,
    )
    if question:
        question.display_a = question.get_option_a(lang)
        question.display_b = question.get_option_b(lang)
    return render(request, 'sound_games/partials/choice_question.html', {
        'question': question, 'lang': lang,
    })


@require_active_game('choice-chaos')
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


@require_active_game('mimic-mayhem')
def mimic_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='mimic-mayhem')
    sound = get_shuffled_item(
        request, 'deck_mimic',
        SoundFX.objects.all(),
    )
    return render(request, 'sound_games/mimic.html', {
        'genre': genre, 'sound': sound, 'lang': lang,
    })


@require_active_game('mimic-mayhem')
def mimic_next(request, lang):
    sound = get_shuffled_item(
        request, 'deck_mimic',
        SoundFX.objects.all(),
        advance=True,
    )
    return render(request, 'sound_games/partials/mimic_sound.html', {
        'sound': sound, 'lang': lang,
    })


@require_active_game('lip-sync-legends')
def lip_sync_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='lip-sync-legends')
    sound = get_shuffled_item(
        request, 'deck_lipsync',
        LipSyncSound.objects.all(),
    )
    if sound:
        sound.display_description = sound.get_description(lang)
    return render(request, 'sound_games/lip_sync.html', {
        'genre': genre, 'sound': sound, 'lang': lang,
    })


@require_active_game('lip-sync-legends')
def lip_sync_next(request, lang):
    sound = get_shuffled_item(
        request, 'deck_lipsync',
        LipSyncSound.objects.all(),
        advance=True,
    )
    if sound:
        sound.display_description = sound.get_description(lang)
    return render(request, 'sound_games/partials/lip_sync_sound.html', {
        'sound': sound, 'lang': lang,
    })
