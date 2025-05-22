from django.test import TestCase
from .models import Categoria, Produto

class LojaTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Teste")
        
    def test_criacao_produto(self):
        produto = Produto.objects.create(
            nome="Produto Teste",
            preco=100.00,
            categoria=self.categoria
        )
        self.assertEqual(str(produto), "Produto Teste")