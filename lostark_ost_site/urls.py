from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),  # ✅ 이 줄 반드시 필요
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


