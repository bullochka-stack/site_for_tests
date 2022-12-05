from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('_nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('', include('tests.urls')),

]

# для отладочного режима только
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
