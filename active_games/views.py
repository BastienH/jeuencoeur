import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.utils import timezone
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import AnalyticsEvent, Genre
from games.utils import apply_age_filter, get_default_age, get_shuffled_item, require_active_game

from .models import CarGame, RoleActivity, RoleCharacter, RoleSetting, TripSession


@require_active_game('wild-roles')
def wild_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='wild-roles')
    character = get_shuffled_item(
        request, 'deck_wild_char',
        RoleCharacter.objects.all(), advance=True,
    )
    setting = get_shuffled_item(
        request, 'deck_wild_set',
        RoleSetting.objects.all(), advance=True,
    )
    activity = get_shuffled_item(
        request, 'deck_wild_act',
        RoleActivity.objects.all(), advance=True,
    )
    return render(request, 'active_games/wild.html', {
        'genre': genre,
        'character': character.get_text(lang) if character else '',
        'setting': setting.get_text(lang) if setting else '',
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


@require_active_game('wild-roles')
def wild_spin(request, lang):
    activate(lang)
    character = get_shuffled_item(
        request, 'deck_wild_char',
        RoleCharacter.objects.all(), advance=True,
    )
    setting = get_shuffled_item(
        request, 'deck_wild_set',
        RoleSetting.objects.all(), advance=True,
    )
    activity = get_shuffled_item(
        request, 'deck_wild_act',
        RoleActivity.objects.all(), advance=True,
    )
    return render(request, 'active_games/partials/wild_results.html', {
        'character': character.get_text(lang) if character else '',
        'setting': setting.get_text(lang) if setting else '',
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


@require_active_game('wild-roles')
def wild_spin_character(request, lang):
    activate(lang)
    character = get_shuffled_item(
        request, 'deck_wild_char',
        RoleCharacter.objects.all(), advance=True,
    )
    return render(request, 'active_games/partials/wild_character.html', {
        'character': character.get_text(lang) if character else '',
        'lang': lang,
    })


@require_active_game('wild-roles')
def wild_spin_setting(request, lang):
    activate(lang)
    setting = get_shuffled_item(
        request, 'deck_wild_set',
        RoleSetting.objects.all(), advance=True,
    )
    return render(request, 'active_games/partials/wild_setting.html', {
        'setting': setting.get_text(lang) if setting else '',
        'lang': lang,
    })


@require_active_game('wild-roles')
def wild_spin_activity(request, lang):
    activate(lang)
    activity = get_shuffled_item(
        request, 'deck_wild_act',
        RoleActivity.objects.all(), advance=True,
    )
    return render(request, 'active_games/partials/wild_activity.html', {
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


@require_active_game('wild-roles')
def wild_react(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    AnalyticsEvent.objects.create(
        event_type='wild_reaction',
        genre=get_object_or_404(Genre, slug='wild-roles'),
        metadata={'reaction': data.get('reaction', '')},
        language=lang,
    )
    return JsonResponse({'status': 'ok'})


@require_active_game('highway-hijinks')
def highway_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='highway-hijinks')
    age_group = request.GET.get('age_group')
    qs = apply_age_filter(CarGame.objects.all(), age_group, age_field='min_age')
    car_game = get_shuffled_item(
        request, 'deck_highway', qs, advance=True,
    )
    trip_active = TripSession.objects.filter(
        user=request.user if request.user.is_authenticated else None,
        active=True,
    ).exists()
    return render(request, 'active_games/highway.html', {
        'genre': genre, 'car_game': car_game, 'lang': lang, 'trip_active': trip_active,
        'reroll_url': reverse('highway_hijinks_next_game', kwargs={'lang': lang}),
        'default_age': get_default_age(request),
    })


@require_active_game('highway-hijinks')
def highway_boredom_buster(request, lang):
    car_game = get_shuffled_item(
        request, 'deck_highway',
        CarGame.objects.all(), advance=True,
    )
    return render(request, 'active_games/partials/highway_game.html', {
        'car_game': car_game, 'lang': lang,
    })


@require_active_game('highway-hijinks')
def highway_next_game(request, lang):
    activate(lang)
    age_group = request.GET.get('age_group')
    filters = {}
    qs = apply_age_filter(CarGame.objects.all(), age_group, age_field='min_age')
    if age_group and age_group != 'all':
        filters['age_group'] = age_group
    car_game = get_shuffled_item(
        request, 'deck_highway', qs,
        filters=filters or None, advance=True,
    )
    return render(request, 'active_games/partials/highway_game.html', {
        'car_game': car_game, 'lang': lang,
    })


@require_active_game('highway-hijinks')
def highway_start_trip(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    session = TripSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        start_lat=data.get('lat'),
        start_lon=data.get('lon'),
        total_distance_km=float(data.get('distance', 0)),
        language=lang,
    )
    return JsonResponse({'status': 'ok', 'trip_id': session.id})


@require_active_game('highway-hijinks')
@require_POST
def highway_update_progress(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    trip = TripSession.objects.filter(id=data.get('trip_id'), active=True).first()
    if trip:
        pct = int(data.get('progress', trip.progress_pct))
        trip.progress_pct = max(0, min(pct, 100))
        trip.save()
    return JsonResponse({'status': 'ok'})


@require_active_game('highway-hijinks')
@require_POST
def highway_end_trip(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    TripSession.objects.filter(id=data.get('trip_id'), active=True).update(
        active=False,
        end_time=timezone.now(),
        progress_pct=100,
    )
    return JsonResponse({'status': 'ok'})
