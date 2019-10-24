from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


def home(request):
    context = {
        'title': 'Hello Word!',
        'content': 'Welcome to the homepage.',
        'premium_content': '',
        'users': User.objects.filter(is_active=True)
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'Hi, my new friends!))'
    return render(request, 'home.html', context)


def about(request):
    context = {
        'title': "About page"
    }
    return render(request, 'home.html', context)


def contact(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Contact page",
        'content': 'Welcome to the contact page',
        'form': contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        messages.success(request, 'Ok, action is right')
        return render(request, 'contact.html', context)
    else:
        messages.error(request, 'Please, try again')

    return render(request, 'home.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # context['form'] = LoginForm()
            return redirect('/')
        else:
            print('Error')
    return render(request, 'login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,

    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)

        return redirect('/')
    return render(request, 'registration.html', context)
