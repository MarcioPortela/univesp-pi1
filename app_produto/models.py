from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)  # Campo para a imagem
    detalhes = models.TextField(blank=True, null=True)  # Campo para os detalhes do produto

    def __str__(self):
        return self.nome
