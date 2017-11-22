# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from my_magazine.models import Category, Brands
from my_magazine.forms import  BrandsForm

def login(request):
    brands_form = BrandsForm
    args = {}
    args['projects'] = Category.objects.all()
    args['form_brands'] = brands_form
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('loginsys/login.html', args)
    else:
        return render_to_response('loginsys/login.html', args)

def logout(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(return_path)

def register(request):
    brands_form = BrandsForm
    args = {}
    args['projects'] = Category.objects.all()
    args['form_brands'] = brands_form
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('loginsys/register.html', args)