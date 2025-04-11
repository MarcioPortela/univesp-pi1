from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Produto

def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))  # Obtém a quantidade do formulário
        request.session['carrinho'] = request.session.get('carrinho', {})
        if str(produto.pk) in request.session['carrinho']:
            request.session['carrinho'][str(produto.pk)] += quantidade
        else:
            request.session['carrinho'][str(produto.pk)] = quantidade
        request.session.modified = True
        messages.success(request, f'{quantidade} unidade(s) de "{produto.nome}" adicionada(s) ao carrinho!')
        return redirect('produto_detalhe', pk=produto.pk)  # Redireciona para a mesma página

    return render(request, 'app_produto/produto_detalhe.html', {'produto': produto})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'app_produto/lista_produtos.html', {'produtos': produtos})

def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    produtos = Produto.objects.filter(pk__in=carrinho.keys())
    itens = [{'produto': produto, 'quantidade': carrinho[str(produto.pk)]} for produto in produtos]
    return render(request, 'app_produto/carrinho.html', {'itens': itens})
