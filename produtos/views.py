from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Get related products
    related_products = Product.objects.filter(
        Q(name__icontains=product.name.split()[0]) | 
        Q(description__icontains=product.name.split()[0])
    ).exclude(id=product.id)[:4]
    
    return render(request, 'produtos/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def product_list(request):
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', '-created_at')
    
    products = Product.objects.all()
    
    # Apply search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    if sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'produtos/product_list.html', {
        'products': products,
        'search_query': search_query,
        'current_sort': sort
    })