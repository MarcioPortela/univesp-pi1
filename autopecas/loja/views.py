from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Produto, Categoria, Carrinho, ItemCarrinho
from .forms import ProdutoForm, CategoriaForm

# Páginas públicas
def lista_produtos(request):
    produtos = Produto.objects.all()  # Ou sua lógica específica
    #return render(request, 'loja/lista_produtos.html', {'produtos': produtos})
    
    #produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria__id=categoria_id)
    
    busca = request.GET.get('busca')
    if busca:
        produtos = produtos.filter(nome__icontains=busca)
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
    }
    return render(request, 'loja/lista_produtos.html', context)

def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    context = {'produto': produto}
    return render(request, 'loja/detalhe_produto.html', context)

# Carrinho
#@login_required
def carrinho(request):
    carrinho, created = Carrinho.objects.get_or_create(
        usuario=request.user, 
        finalizado=False
    )
    return render(request, 'loja/carrinho.html', {'carrinho': carrinho})

#@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    carrinho, created = Carrinho.objects.get_or_create(
        usuario=request.user, 
        finalizado=False
    )
    
    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1}
    )
    
    if not created:
        if item.quantidade < produto.estoque:
            item.quantidade += 1
            item.save()
            messages.success(request, f"Quantidade de {produto.nome} atualizada no carrinho!")
        else:
            messages.warning(request, f"Quantidade máxima em estoque atingida para {produto.nome}!")
    else:
        messages.success(request, f"{produto.nome} adicionado ao carrinho!")
    
    return redirect('carrinho')

#@login_required
def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id, carrinho__usuario=request.user)
    produto_nome = item.produto.nome
    item.delete()
    messages.success(request, f"{produto_nome} removido do carrinho!")
    return redirect('carrinho')

#@login_required
def atualizar_carrinho(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrinho, pk=item_id, carrinho__usuario=request.user)
        quantidade = int(request.POST.get('quantidade', 1))
        
        if quantidade > 0 and quantidade <= item.produto.estoque:
            item.quantidade = quantidade
            item.save()
            messages.success(request, "Quantidade atualizada!")
        elif quantidade > item.produto.estoque:
            messages.warning(request, f"Quantidade solicitada maior que o estoque disponível ({item.produto.estoque})")
        else:
            item.delete()
            messages.success(request, "Item removido do carrinho!")
    
    return redirect('carrinho')

# CRUD Produtos
@permission_required('loja.change_produto')
def lista_produtos_admin(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/admin/lista_produtos_admin.html', {'produtos': produtos})

@permission_required('loja.add_produto')
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto adicionado com sucesso!")
            return redirect('lista_produtos_admin')
    else:
        form = ProdutoForm()
    
    return render(request, 'loja/admin/produto_form.html', {'form': form, 'titulo': 'Adicionar Produto'})

@permission_required('loja.change_produto')
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect('lista_produtos_admin')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'loja/admin/produto_form.html', {'form': form, 'titulo': 'Editar Produto'})

@permission_required('loja.delete_produto')
def remover_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, "Produto removido com sucesso!")
        return redirect('lista_produtos_admin')
    
    return render(request, 'loja/admin/confirmar_remocao.html', {
        'objeto': produto,
        'tipo': 'produto'
    })

# CRUD Categorias
@permission_required('loja.change_categoria')
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'loja/admin/lista_categorias.html', {'categorias': categorias})

@permission_required('loja.add_categoria')
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria adicionada com sucesso!")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'loja/admin/categoria_form.html', {'form': form, 'titulo': 'Adicionar Categoria'})

@permission_required('loja.change_categoria')
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'loja/admin/categoria_form.html', {'form': form, 'titulo': 'Editar Categoria'})

@permission_required('loja.delete_categoria')
def remover_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoria removida com sucesso!")
        return redirect('lista_categorias')
    
    return render(request, 'loja/admin/confirmar_remocao.html', {
        'objeto': categoria,
        'tipo': 'categoria'
    })