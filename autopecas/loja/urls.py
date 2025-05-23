from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('produto/<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('atualizar/<int:item_id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    
    # URLs administrativas
    path('admin/produtos/', views.lista_produtos_admin, name='lista_produtos_admin'),
    path('admin/produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('admin/produtos/editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('admin/produtos/remover/<int:pk>/', views.remover_produto, name='remover_produto'),
]