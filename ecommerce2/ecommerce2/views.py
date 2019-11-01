from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .forms import *


def home(request):
    context = {
        'title': 'Hello Word!',
        'content': 'Welcome to the homepage.',
        'premium_content': '',
        'users': User.objects.filter(active=True)
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
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    #     messages.success(request, 'Ok, action is right')
    #     return render(request, 'contact.html', context)
    # else:
    #     messages.error(request, 'Please, try again')

    return render(request, 'home.html', context)



