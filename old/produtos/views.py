from django.shortcuts import render

def carrinho_view(request):
    # Dados de exemplo (substitua depois pelos seus modelos reais)
    context = {
        'itens_carrinho': [
            {
                'produto': {
                    'nome': 'Produto Exemplo',
                    'preco': '99.99',
                    'imagem': {'url': ''}
                },
                'quantidade': 2
            }
        ],
        'carrinho': {
            'subtotal': '99.99',
            'frete': '0.00',
            'desconto': '0.00',
            'total': '99.99'
        }
    }
    return render(request, 'produtos/carrinho.html', context)