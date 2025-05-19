from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfileForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db import transaction

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

login_view = CustomLoginView.as_view()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    # Add Bootstrap classes to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'usuarios/register.html', {'form': form})

@login_required
def account(request):
    return render(request, 'usuarios/account.html')

@login_required
def orders(request):
    # Implemente a lógica para buscar pedidos do usuário
    return render(request, 'usuarios/orders.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('account')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'usuarios/edit_profile.html', {
        'form': form,
        'states': ProfileForm.STATE_CHOICES
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('account')
    else:
        form = PasswordChangeForm(request.user)
    
    # Add Bootstrap classes to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'usuarios/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            try:
                with transaction.atomic():
                    request.user.favorite_set.all().delete()
                    request.user.delete()
                messages.success(request, 'Sua conta foi excluída com sucesso! Esperamos ver você novamente.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Ocorreu um erro ao excluir sua conta. Por favor, tente novamente.')
                return redirect('account')
        else:
            messages.error(request, 'Senha incorreta. Por favor, tente novamente.')
    
    return render(request, 'usuarios/delete_account.html')

@login_required
def favorites(request):
    # Get user's favorites - implement this based on your model structure
    favorites = []  # Replace with actual favorites query
    return render(request, 'usuarios/favorites.html', {
        'favorites': favorites
    })

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def home(request):
    return render(request, 'usuarios/home.html')  # Ensure you have a 'home.html' template