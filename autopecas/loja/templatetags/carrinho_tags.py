from django import template
register = template.Library()

@register.simple_tag
def carrinho_ativo(user):
    return user.carrinho_set.filter(finalizado=False).first()