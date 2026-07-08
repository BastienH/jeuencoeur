import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AnalyticsEvent, Favorite, Genre, Prompt, UserProfile
from .utils import is_tester


def _favorited(prompt, request):
    if request.user.is_authenticated:
        return Favorite.objects.filter(user=request.user, prompt=prompt).exists()
    return False


def hub(request, lang):
    activate(lang)
    genres = list(Genre.objects.all())
    if request.user.is_authenticated:
        try:
            order = request.user.profile.settings.get('game_order', {})
            if order:
                genres.sort(key=lambda g: order.get(g.slug, 999))
        except AttributeError:
            pass
    return render(request, 'hub.html', {
        'genres': genres, 'lang': lang,
        'is_tester': is_tester(request.user),
    })


def detail(request, lang, genre_slug):
    activate(lang)
    genre = get_object_or_404(Genre, slug=genre_slug)
    if not genre.is_active and not is_tester(request.user):
        return redirect('hub', lang=lang)
    prompt = Prompt.objects.get_random(genre, lang)
    return render(request, 'detail.html', {
        'genre': genre,
        'prompt': prompt,
        'lang': lang,
        'is_favorited': _favorited(prompt, request) if prompt else False,
    })


def next_prompt(request, lang):
    activate(lang)
    genre_slug = request.GET.get('genre_slug')
    genre = get_object_or_404(Genre, slug=genre_slug)
    prompt = Prompt.objects.get_random(genre, lang)
    return render(request, 'partials/prompt_card.html', {
        'prompt': prompt,
        'genre': genre,
        'lang': lang,
        'is_favorited': _favorited(prompt, request) if prompt else False,
    })


def signup(request, lang):
    activate(lang)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created!')
            next_url = request.GET.get('next') or request.POST.get('next') or ''
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                return redirect(next_url)
            return redirect('hub', lang=lang)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'lang': lang})


def login_view(request, lang):
    activate(lang)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or ''
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                return redirect(next_url)
            return redirect('hub', lang=lang)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'lang': lang})


def logout_view(request, lang):
    logout(request)
    return redirect('hub', lang=lang)


@login_required
def profile(request, lang):
    activate(lang)
    favorites = Favorite.objects.filter(user=request.user).select_related('prompt__genre')
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    genres = Genre.objects.all()

    if request.method == 'POST':
        raw = request.POST.get('game_order', '')
        order_map = {}
        for i, slug in enumerate(raw.split(',')):
            slug = slug.strip()
            if slug:
                order_map[slug] = i
        settings = profile_obj.settings
        if order_map:
            settings['game_order'] = order_map
        else:
            settings.pop('game_order', None)
        profile_obj.settings = settings
        profile_obj.save(update_fields=['settings'])

    return render(request, 'profile.html', {
        'lang': lang,
        'favorites': favorites,
        'profile': profile_obj,
        'genres': genres,
    })


@login_required
@require_POST
def toggle_favorite(request, lang, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, prompt=prompt)
    if not created:
        favorite.delete()
    return render(request, 'partials/favorite_heart.html', {
        'prompt': prompt,
        'is_favorited': created,
        'lang': lang,
    })


@csrf_exempt
@require_POST
def track_event(request, lang):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST.dict()

    event_type = data.get('event_type', '')
    if event_type not in dict(AnalyticsEvent.EVENT_TYPES):
        from django.http import JsonResponse
        return JsonResponse({'error': 'invalid event_type'}, status=400)

    AnalyticsEvent.objects.create(
        event_type=event_type,
        genre_id=data.get('genre_id'),
        prompt_id=data.get('prompt_id'),
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key or '',
        language=lang,
        metadata=data.get('metadata', {}),
        ip_address=request.META.get('REMOTE_ADDR'),
    )
    from django.http import JsonResponse
    return JsonResponse({'status': 'ok'})


def print_deck_list(request, lang):
    activate(lang)
    genres = Genre.objects.exclude(game_module='').order_by('name')
    return render(request, 'print_deck_list.html', {'genres': genres, 'lang': lang})


def print_deck_pdf(request, lang, game_module):
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    activate(lang)
    genre = get_object_or_404(Genre, game_module=game_module)
    entries = get_printable_entries(game_module, lang)
    html = render_to_string('print_deck_pdf.html', {
        'genre': genre, 'entries': entries, 'lang': lang,
    })
    try:
        from weasyprint import HTML
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{genre.slug}-deck.pdf"'
        return response
    except ImportError:
        return HttpResponse(html)


def get_printable_entries(game_module, lang):
    if game_module == 'giggle_generators':
        from sound_games.models import MicroChallenge
        return [{'text': c.get_text(lang), 'meta': f'{c.age_group}/{c.energy_level}'}
                for c in MicroChallenge.objects.all()[:50]]
    if game_module == 'choice_chaos':
        from sound_games.models import WYRQuestion
        return [{'text': f'{q.get_option_a(lang)} vs {q.get_option_b(lang)}', 'meta': q.category}
                for q in WYRQuestion.objects.all()[:50]]
    if game_module == 'tale_twisters':
        from creative_games.models import StoryTwist
        return [{'text': t.get_text(lang)} for t in StoryTwist.objects.all()[:50]]
    if game_module == 'mimic_mayhem':
        from sound_games.models import SoundFX
        return [{'text': s.name} for s in SoundFX.objects.all()[:50]]
    if game_module == 'wild_roles':
        chars = list(RoleCharacter.objects.all()[:20])
        from active_games.models import RoleCharacter, RoleSetting, RoleActivity
        chars = [c.get_text(lang) for c in RoleCharacter.objects.all()[:20]]
        sets = [s.get_text(lang) for s in RoleSetting.objects.all()[:20]]
        acts = [a.get_text(lang) for a in RoleActivity.objects.all()[:20]]
        return [{'text': f'{c} + {s} + {a}'} for c, s, a in zip(chars, sets, acts)]
    if game_module == 'funny_face_factory':
        from creative_games.models import FacePrompt
        return [{'text': p.get_text(lang)} for p in FacePrompt.objects.all()[:50]]
    if game_module == 'lip_sync_legends':
        from sound_games.models import LipSyncSound
        return [{'text': s.get_description(lang) or s.name} for s in LipSyncSound.objects.all()[:50]]
    if game_module == 'highway_hijinks':
        from active_games.models import CarGame
        return [{'text': c.instructions_en[:200], 'meta': c.name_en} for c in CarGame.objects.all()[:50]]
    if game_module == 'doodle_dash':
        subs = list(DoodleSubject.objects.all()[:20])
        from creative_games.models import DoodleAccessory, DoodleEmotion, DoodleSubject
        subs = [s.get_text(lang) for s in DoodleSubject.objects.all()[:20]]
        emos = [e.get_text(lang) for e in DoodleEmotion.objects.all()[:20]]
        accs = [a.get_text(lang) for a in DoodleAccessory.objects.all()[:20]]
        return [{'text': f'{s} + {e} + {a}'} for s, e, a in zip(subs, emos, accs)]
    return []
