from django.contrib import admin
from django.urls import include, re_path
from questions.views import IndexView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^questions/', include('questions.urls')),
    re_path(r'^core/', include('core.urls')),
    re_path(r'^$', IndexView.as_view(), name="index_question_view")
]

from django.conf import settings 
from django.conf.urls.static import static 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    print(f"DEBUG: Media URL enabled: {settings.MEDIA_URL}")
    print(f"DEBUG: Media ROOT: {settings.MEDIA_ROOT}")