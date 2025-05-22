from .models import Carrinho

def carrinho(request):
    if request.user.is_authenticated:
        carrinho, created = Carrinho.objects.get_or_create(
            usuario=request.user,
            finalizado=False
        )
        return {'carrinho': carrinho}
    return {'carrinho': None}