from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("<h1>Bem-vindo à página inicial!</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Página inicial
    path('', include('app_produto.urls')),  # Inclui as rotas do app_produto sem prefixo
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
