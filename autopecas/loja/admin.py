from django.contrib import admin
from .models import Produto, Categoria, Carrinho, ItemCarrinho

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria', 'estoque')
    search_fields = ('nome', 'descricao')
    list_filter = ('categoria', 'ativo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Registre outros modelos conforme necessário
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)