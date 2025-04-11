# filepath: c:\Users\Principal\Downloads\telaproduto\app_produto\admin.py
from django.contrib import admin
from .models import Produto

admin.site.register(Produto)