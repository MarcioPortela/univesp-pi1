from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('lista_categorias')

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='produtos')
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    estoque = models.PositiveIntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('detalhe_produto', kwargs={'pk': self.pk})

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    finalizado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
        ordering = ['-criado_em']
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())
    
    def __str__(self):
        return f"Carrinho #{self.id} - {self.usuario.username}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        ordering = ['-adicionado_em']
        unique_together = ['carrinho', 'produto']
    
    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (R${self.subtotal})"