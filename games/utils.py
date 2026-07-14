import random
from functools import wraps

from django.shortcuts import redirect
from django.utils.translation import activate


def get_shuffled_item(request, session_key, queryset, filters=None, advance=False):
    """
    Get an item from a shuffled deck stored in the Django session.

    Args:
        request:        Django request object
        session_key:    Unique key for this deck (e.g. 'deck_giggle')
        queryset:       Base queryset to draw from
        filters:        Optional dict of active filters; a change triggers reshuffle
        advance:        If True, draw the next item; if False, return the current one

    Returns:
        A model instance or None if the queryset is empty.
    """
    current_filters = filters or {}
    deck = request.session.get(session_key)
    reshuffle = False

    if not (deck and deck.get('filters') == current_filters):
        reshuffle = True
    elif advance:
        index = deck['index']
        if index >= len(deck['ids']):
            reshuffle = True

    if reshuffle:
        ids = list(queryset.values_list('id', flat=True))
        if not ids:
            request.session.pop(session_key, None)
            return None
        random.shuffle(ids)
        deck = {
            'ids': ids,
            'index': 0,
            'filters': current_filters,
            'current_id': None,
        }

    if advance or deck.get('current_id') is None:
        index = deck['index']
        if index >= len(deck['ids']):
            ids = list(queryset.values_list('id', flat=True))
            if not ids:
                request.session.pop(session_key, None)
                return None
            random.shuffle(ids)
            deck['ids'] = ids
            index = 0

        item_id = deck['ids'][index]
        deck['index'] = index + 1
        deck['current_id'] = item_id
    else:
        item_id = deck['current_id']

    request.session[session_key] = deck
    request.session.modified = True

    return queryset.filter(id=item_id).first()


def is_tester(user):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.settings.get('is_tester', False)
    except AttributeError:
        return False


def require_active_game(genre_slug):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from .models import Genre
            lang = kwargs.get('lang', 'en')
            activate(lang)
            try:
                genre = Genre.objects.get(slug=genre_slug)
            except Genre.DoesNotExist:
                return redirect('hub', lang=lang)
            if not genre.is_active and not is_tester(request.user):
                return redirect('hub', lang=lang)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


AGE_ORDER = ['3-6', '7-10', '11+']


def get_default_age(request):
    if request.user.is_authenticated:
        from .models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return profile.settings.get('default_age', 'all')
    return 'all'


def apply_age_filter(qs, age_value, age_field='age_group'):
    """Apply min_age filtering: show content for this age AND younger."""
    if not age_value or age_value == 'all':
        return qs
    idx = AGE_ORDER.index(age_value)
    allowed = ['all'] + AGE_ORDER[:idx + 1]
    return qs.filter(**{f'{age_field}__in': allowed})
