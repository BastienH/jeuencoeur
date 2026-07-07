import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from games.models import Genre, StorySeed

from .models import (DoodleAccessory, DoodleDrawing, DoodleEmotion,
                     DoodleSubject, FacePrompt, StoryEnding, StorySession, StoryTwist)


def tale_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='tale-twisters')
    twist = StoryTwist.get_random(lang)
    return render(request, 'creative_games/tale.html', {
        'genre': genre, 'twist': twist, 'lang': lang,
    })


def tale_twist(request, lang):
    activate(lang)
    twist = StoryTwist.get_random(lang)
    return render(request, 'creative_games/partials/tale_twist.html', {
        'twist': twist, 'lang': lang,
    })


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
            'used_twists': request.session.get(session_key, {}).get('used_twists', []),
        }
        request.session.modified = True
        return JsonResponse({'status': 'ok', 'phase': 'twist'})
    seeds = list(StorySeed.objects.filter(genre__slug='tale-twisters').order_by('?')[:3])
    for s in seeds:
        s.display_text = s.get_text(lang)
    return render(request, 'creative_games/partials/tale_start.html', {
        'seeds': seeds, 'lang': lang,
    })


def tale_pick_twist(request, lang):
    activate(lang)
    if request.method == 'POST':
        data = json.loads(request.body) if request.body else request.POST
        twist_id = data.get('twist_id')
        session_key = f'tale_{lang}'
        state = request.session.get(session_key, {})
        used = list(state.get('used_twists', []))
        used.append(int(twist_id))
        state['twist_id'] = int(twist_id)
        state['used_twists'] = used
        request.session[session_key] = state
        request.session.modified = True
        return JsonResponse({'status': 'ok', 'phase': 'ending'})
    used = request.session.get(f'tale_{lang}', {}).get('used_twists', [])
    twists = list(StoryTwist.objects.filter(genre__slug='tale-twisters').exclude(id__in=used).order_by('?')[:3])
    for t in twists:
        t.display_text = t.get_text(lang)
    return render(request, 'creative_games/partials/tale_twist_options.html', {
        'twists': twists, 'lang': lang,
    })


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
    endings = list(StoryEnding.objects.filter(genre__slug='tale-twisters').order_by('?')[:3])
    for e in endings:
        e.display_text = e.get_text(lang)
    return render(request, 'creative_games/partials/tale_ending_options.html', {
        'endings': endings, 'lang': lang,
    })


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


def tale_save(request, lang):
    data = json.loads(request.body) if request.body else request.POST
    session = StorySession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        title=data.get('title', ''),
        content=data.get('content', ''),
        duration_seconds=int(data.get('duration', 0)),
        language=lang,
    )
    if 'audio' in request.FILES:
        session.audio_file = request.FILES['audio']
        session.save()
    return JsonResponse({'status': 'ok', 'id': session.id})


def tale_vault(request, lang):
    activate(lang)
    sessions = StorySession.objects.filter(user=request.user) if request.user.is_authenticated else StorySession.objects.none()
    return render(request, 'creative_games/tale_vault.html', {
        'sessions': sessions, 'lang': lang,
    })


def funny_face_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='funny-face-factory')
    prompt = FacePrompt.get_random(lang)
    return render(request, 'creative_games/funny_face.html', {
        'genre': genre, 'prompt': prompt, 'lang': lang,
    })


def funny_face_next(request, lang):
    activate(lang)
    prompt = FacePrompt.get_random(lang)
    return render(request, 'creative_games/partials/funny_face_prompt.html', {
        'prompt': prompt, 'lang': lang,
    })


def doodle_play(request, lang):
    activate(lang)
    genre = get_object_or_404(Genre, slug='doodle-dash')
    from .models import DoodleAccessory, DoodleEmotion, DoodleSubject
    subj = DoodleSubject.objects.order_by('?').first()
    emot = DoodleEmotion.objects.order_by('?').first()
    acc = DoodleAccessory.objects.order_by('?').first()
    prompt = {
        'subject': subj.get_text(lang) if subj else '',
        'emotion': emot.get_text(lang) if emot else '',
        'accessory': acc.get_text(lang) if acc else '',
    }
    return render(request, 'creative_games/doodle.html', {
        'genre': genre, 'prompt': prompt, 'lang': lang,
    })


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


def doodle_gallery(request, lang):
    activate(lang)
    drawings = DoodleDrawing.objects.all().order_by('-created_at')[:20]
    return render(request, 'creative_games/doodle_gallery.html', {
        'drawings': drawings, 'lang': lang,
    })
