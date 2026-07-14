import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import Genre, StorySeed
from games.utils import get_shuffled_item, require_active_game

from .models import (DoodleAccessory, DoodleDrawing, DoodleEmotion,
                     DoodleSubject, FacePrompt, StoryEnding, StorySession, StoryTwist)


@require_active_game('tale-twisters')
def tale_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='tale-twisters')
    twist = get_shuffled_item(
        request, 'deck_tale_twist',
        StoryTwist.objects.filter(genre__slug='tale-twisters'),
    )
    if twist:
        twist.display_text = twist.get_text(lang)
    return render(request, 'creative_games/tale.html', {
        'genre': genre, 'twist': twist, 'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_twist(request, lang):
    activate(lang)
    twist = get_shuffled_item(
        request, 'deck_tale_twist',
        StoryTwist.objects.filter(genre__slug='tale-twisters'),
        advance=True,
    )
    if twist:
        twist.display_text = twist.get_text(lang)
    return render(request, 'creative_games/partials/tale_twist.html', {
        'twist': twist, 'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_start(request, lang):
    activate(lang)
    if request.method == 'POST':
        data = json.loads(request.body) if request.body else request.POST
        seed_id = data.get('seed_id')
        session_key = f'tale_{lang}'
        request.session[session_key] = {
            'seed_id': int(seed_id),
            'twist_id': None,
            'ending_id': None,
        }
        request.session.modified = True
        return JsonResponse({'status': 'ok', 'phase': 'twist'})
    seeds = []
    for _ in range(3):
        seed = get_shuffled_item(
            request, 'deck_tale_seed',
            StorySeed.objects.filter(genre__slug='tale-twisters'),
            advance=True,
        )
        if seed:
            seed.display_text = seed.get_text(lang)
            seeds.append(seed)
    return render(request, 'creative_games/partials/tale_start.html', {
        'seeds': seeds, 'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_pick_twist(request, lang):
    activate(lang)
    if request.method == 'POST':
        data = json.loads(request.body) if request.body else request.POST
        twist_id = data.get('twist_id')
        session_key = f'tale_{lang}'
        state = request.session.get(session_key, {})
        state['twist_id'] = int(twist_id)
        request.session[session_key] = state
        request.session.modified = True
        return JsonResponse({'status': 'ok', 'phase': 'ending'})
    twists = []
    for _ in range(3):
        twist = get_shuffled_item(
            request, 'deck_tale_twist',
            StoryTwist.objects.filter(genre__slug='tale-twisters'),
            advance=True,
        )
        if twist:
            twist.display_text = twist.get_text(lang)
            twists.append(twist)
    return render(request, 'creative_games/partials/tale_twist_options.html', {
        'twists': twists, 'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_pick_ending(request, lang):
    activate(lang)
    if request.method == 'POST':
        data = json.loads(request.body) if request.body else request.POST
        ending_id = data.get('ending_id')
        session_key = f'tale_{lang}'
        state = request.session.get(session_key, {})
        state['ending_id'] = int(ending_id)
        request.session[session_key] = state
        request.session.modified = True
        return JsonResponse({'status': 'ok', 'phase': 'complete'})
    endings = []
    for _ in range(3):
        ending = get_shuffled_item(
            request, 'deck_tale_ending',
            StoryEnding.objects.filter(genre__slug='tale-twisters'),
            advance=True,
        )
        if ending:
            ending.display_text = ending.get_text(lang)
            endings.append(ending)
    return render(request, 'creative_games/partials/tale_ending_options.html', {
        'endings': endings, 'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_state(request, lang):
    activate(lang)
    session_key = f'tale_{lang}'
    state = request.session.get(session_key, {})
    seed_id = state.get('seed_id')
    twist_id = state.get('twist_id')
    ending_id = state.get('ending_id')
    seed = StorySeed.objects.filter(id=seed_id).first()
    twist = StoryTwist.objects.filter(id=twist_id).first()
    ending = StoryEnding.objects.filter(id=ending_id).first()
    return render(request, 'creative_games/partials/tale_story_display.html', {
        'seed': seed.get_text(lang) if seed else None,
        'twist': twist.get_text(lang) if twist else None,
        'ending': ending.get_text(lang) if ending else None,
        'phase': 'complete' if ending_id else ('twist_locked' if twist_id else ('seed_locked' if seed_id else 'start')),
        'lang': lang,
    })


@require_active_game('tale-twisters')
def tale_save(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    title = strip_tags(data.get('title', ''))
    content = strip_tags(data.get('content', ''))
    if not request.user.is_authenticated:
        request.session['pending_story'] = {
            'title': title,
            'content': content,
            'duration_seconds': int(data.get('duration', 0)),
            'language': lang,
        }
        login_url = reverse('login', kwargs={'lang': lang})
        next_url = reverse('tale_twisters_claim_story', kwargs={'lang': lang})
        return JsonResponse({
            'status': 'login_required',
            'login_url': f'{login_url}?next={next_url}',
        })
    session = StorySession.objects.create(
        user=request.user,
        title=title,
        content=content,
        duration_seconds=int(data.get('duration', 0)),
        language=lang,
    )
    if 'audio' in request.FILES:
        session.audio_file = request.FILES['audio']
        session.save()
    return JsonResponse({'status': 'ok', 'id': session.id})


@require_active_game('tale-twisters')
def tale_chest(request, lang):
    activate(lang)
    if not request.user.is_authenticated:
        login_url = reverse('login', kwargs={'lang': lang})
        next_url = reverse('tale_twisters_chest', kwargs={'lang': lang})
        return redirect(f'{login_url}?next={next_url}')
    sessions = StorySession.objects.filter(user=request.user)
    genre = get_object_or_404(Genre, slug='tale-twisters')
    return render(request, 'creative_games/tale_chest.html', {
        'sessions': sessions, 'lang': lang, 'genre': genre,
    })


@require_active_game('tale-twisters')
def tale_claim_story(request, lang):
    activate(lang)
    pending = request.session.pop('pending_story', None)
    if pending and request.user.is_authenticated:
        StorySession.objects.create(
            user=request.user,
            title=pending.get('title', ''),
            content=pending.get('content', ''),
            duration_seconds=pending.get('duration_seconds', 0),
            language=pending.get('language', lang),
        )
    return redirect('tale_twisters_chest', lang=lang)


@require_active_game('funny-face-factory')
def funny_face_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='funny-face-factory')
    age_group = request.GET.get('age')
    category = request.GET.get('cat')
    filters = {}
    if age_group and age_group != 'all':
        filters['age_group'] = age_group
    if category:
        filters['category'] = category
    qs = FacePrompt.objects.all()
    if age_group and age_group != 'all':
        qs = qs.filter(age_group=age_group)
    if category:
        qs = qs.filter(category=category)
    prompt = get_shuffled_item(
        request, 'deck_funny', qs,
        filters=filters or None,
    )
    if prompt:
        prompt.display_text = prompt.get_text(lang)
    return render(request, 'creative_games/funny_face.html', {
        'genre': genre, 'prompt': prompt, 'lang': lang,
        'age_group': age_group, 'category': category,
    })


@require_active_game('funny-face-factory')
def funny_face_next(request, lang):
    activate(lang)
    age_group = request.GET.get('age')
    category = request.GET.get('cat')
    filters = {}
    if age_group and age_group != 'all':
        filters['age_group'] = age_group
    if category:
        filters['category'] = category
    qs = FacePrompt.objects.all()
    if age_group and age_group != 'all':
        qs = qs.filter(age_group=age_group)
    if category:
        qs = qs.filter(category=category)
    prompt = get_shuffled_item(
        request, 'deck_funny', qs,
        filters=filters or None, advance=True,
    )
    if prompt:
        prompt.display_text = prompt.get_text(lang)
    return render(request, 'creative_games/partials/funny_face_prompt.html', {
        'prompt': prompt, 'lang': lang,
    })


@require_active_game('doodle-dash')
def doodle_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='doodle-dash')
    subj = get_shuffled_item(
        request, 'deck_doodle_subj',
        DoodleSubject.objects.all(), advance=True,
    )
    emot = get_shuffled_item(
        request, 'deck_doodle_emot',
        DoodleEmotion.objects.all(), advance=True,
    )
    acc = get_shuffled_item(
        request, 'deck_doodle_acc',
        DoodleAccessory.objects.all(), advance=True,
    )
    prompt = {
        'subject': subj.get_text(lang) if subj else '',
        'emotion': emot.get_text(lang) if emot else '',
        'accessory': acc.get_text(lang) if acc else '',
    }
    return render(request, 'creative_games/doodle.html', {
        'genre': genre, 'prompt': prompt, 'lang': lang,
    })


@require_active_game('doodle-dash')
@require_POST
def doodle_save(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    DoodleDrawing.objects.create(
        user=request.user if request.user.is_authenticated else None,
        prompt_subject=data.get('subject', ''),
        prompt_emotion=data.get('emotion', ''),
        prompt_accessory=data.get('accessory', ''),
        image=data.get('image', ''),
        language=lang,
    )
    return JsonResponse({'status': 'ok'})


@require_active_game('doodle-dash')
def doodle_gallery(request, lang):
    activate(lang)
    drawings = DoodleDrawing.objects.all().order_by('-created_at')[:20]
    return render(request, 'creative_games/doodle_gallery.html', {
        'drawings': drawings, 'lang': lang,
    })
