import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import AnalyticsEvent, Genre

from .models import CarGame, RoleActivity, RoleCharacter, RoleSetting, TripSession


def wild_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='wild-roles')
    character = RoleCharacter.objects.order_by('?').first()
    setting = RoleSetting.objects.order_by('?').first()
    activity = RoleActivity.objects.order_by('?').first()
    return render(request, 'active_games/wild.html', {
        'genre': genre,
        'character': character.get_text(lang) if character else '',
        'setting': setting.get_text(lang) if setting else '',
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


def wild_spin(request, lang):
    activate(lang)
    character = RoleCharacter.objects.order_by('?').first()
    setting = RoleSetting.objects.order_by('?').first()
    activity = RoleActivity.objects.order_by('?').first()
    return render(request, 'active_games/partials/wild_results.html', {
        'character': character.get_text(lang) if character else '',
        'setting': setting.get_text(lang) if setting else '',
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


def wild_spin_character(request, lang):
    activate(lang)
    character = RoleCharacter.objects.order_by('?').first()
    return render(request, 'active_games/partials/wild_character.html', {
        'character': character.get_text(lang) if character else '',
        'lang': lang,
    })


def wild_spin_setting(request, lang):
    activate(lang)
    setting = RoleSetting.objects.order_by('?').first()
    return render(request, 'active_games/partials/wild_setting.html', {
        'setting': setting.get_text(lang) if setting else '',
        'lang': lang,
    })


def wild_spin_activity(request, lang):
    activate(lang)
    activity = RoleActivity.objects.order_by('?').first()
    return render(request, 'active_games/partials/wild_activity.html', {
        'activity': activity.get_text(lang) if activity else '',
        'lang': lang,
    })


def wild_react(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    AnalyticsEvent.objects.create(
        event_type='wild_reaction',
        genre=get_object_or_404(Genre, slug='wild-roles'),
        metadata={'reaction': data.get('reaction', '')},
        language=lang,
    )
    return JsonResponse({'status': 'ok'})


def highway_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='highway-hijinks')
    car_game = CarGame.objects.order_by('?').first()
    return render(request, 'active_games/highway.html', {
        'genre': genre, 'car_game': car_game, 'lang': lang,
    })


def highway_boredom_buster(request, lang):
    car_game = CarGame.objects.order_by('?').first()
    return render(request, 'active_games/partials/highway_game.html', {
        'car_game': car_game, 'lang': lang,
    })


def highway_next_game(request, lang):
    activate(lang)
    trip_id = request.GET.get('trip_id')
    if trip_id:
        trip = TripSession.objects.filter(id=trip_id, active=True).first()
    else:
        trip = None
    shown = set(trip.games_shown) if trip else set()
    qs = CarGame.objects.exclude(id__in=shown)
    count = qs.count()
    if count == 0:
        qs = CarGame.objects.all()
        if trip:
            trip.games_shown = []
            trip.save()
    car_game = qs.order_by('?').first()
    if trip and car_game:
        shown.add(car_game.id)
        trip.games_shown = list(shown)
        trip.save()
    return render(request, 'active_games/partials/highway_game.html', {
        'car_game': car_game, 'lang': lang,
    })


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


@require_POST
def highway_update_progress(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    trip = TripSession.objects.filter(id=data.get('trip_id'), active=True).first()
    if trip:
        trip.progress_pct = min(int(data.get('progress', trip.progress_pct)), 100)
        trip.save()
    return JsonResponse({'status': 'ok'})


@require_POST
def highway_end_trip(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    TripSession.objects.filter(id=data.get('trip_id'), active=True).update(
        active=False,
        end_time=timezone.now(),
        progress_pct=100,
    )
    return JsonResponse({'status': 'ok'})
