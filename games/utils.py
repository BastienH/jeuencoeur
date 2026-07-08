from functools import wraps

from django.shortcuts import redirect
from django.utils.translation import activate


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
