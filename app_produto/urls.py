from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('produto/<int:pk>/', views.produto_detalhe, name='produto_detalhe'),  # Rota para detalhes do produto
    path('', views.lista_produtos, name='lista_produtos'),  # Rota para lista de produtos
    path('carrinho/', views.carrinho, name='carrinho'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
