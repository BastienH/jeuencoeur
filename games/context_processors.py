import json

from django.utils import timezone
from django.utils import translation

from .models import Genre


def analytics(request):
    return {
        'analytics_session_key': request.session.session_key or '',
        'analytics_timestamp': int(timezone.now().timestamp()),
    }


def all_genres_data(request):
    from .utils import is_tester
    genres = Genre.objects.exclude(game_module='')
    if not is_tester(request.user):
        genres = genres.filter(is_active=True)
    lang = translation.get_language() or 'en'
    data = [{
        'name': g.get_name(lang),
        'module': g.game_module,
        'slug': g.slug,
    } for g in genres]
    return {'genres_json': json.dumps(data)}
