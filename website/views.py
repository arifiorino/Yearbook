from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Yearbook
import json
import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Yearbook.objects.create(user=request.user,data=[],secretkey=randomString())
            return redirect('yearbook')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_text(request, secretkey=''):
    post = request.POST
    print(post, secretkey)
    return redirect("yearbook")

def yearbook_view(request, secretkey=''):
    y = None

    if secretkey == '':
        y = Yearbook.objects.filter(user=request.user).first()
        print('mine')
    else:
        y = Yearbook.objects.filter(secretkey=secretkey).first()
        print('yours')

    print(y.data)
    texts = json.loads(y.data)

    if request.method == 'POST': # Add text
        post = request.POST
        
        texts.append([[int(post['pointX']),int(post['pointY'])],post['text']])
        y.data=json.dumps(texts)
        y.save()
        return redirect("yearbook")

    context = {'text_points': json.loads(y.data)}
    return render(request, 'draw.html', context)
