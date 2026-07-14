from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from games.views import offline

urlpatterns = [
    path('admin/', admin.site.urls),
    path('offline/', offline, name='offline'),
    path('', RedirectView.as_view(url='/en/', permanent=False)),
    path('<str:lang>/', include('games.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
