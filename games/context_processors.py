from django.utils import timezone


def analytics(request):
    return {
        'analytics_session_key': request.session.session_key or '',
        'analytics_timestamp': int(timezone.now().timestamp()),
    }
