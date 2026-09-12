from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from school_portal import settings

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('forum.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
