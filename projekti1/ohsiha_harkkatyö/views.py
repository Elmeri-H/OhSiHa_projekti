from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Skeittispotti
from .forms import SpottiForm
import requests

url = 'https://data.tampere.fi/data/api/action/datastore_search?resource_id=8a0bce3e-ddf3-4718-a6af-8924c70ebf10'

def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
    '''
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    '''

def home(request):
    spots = Skeittispotti.objects.all()
    response = requests.get(url)
    data = response.json()
    fielddata = data['result']
    fielddata = fielddata['records']
    cleanData = []

    for field in fielddata:
        cleanData.append(field)

    return render(request, 'home.html', {
        'data' : cleanData,
        'spots' : spots
    })

def create_spot(request):
    form = SpottiForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'questions-form.html', {'form': form})

def update_spot(request, id):
    spot = Skeittispotti.objects.get(id=id)
    form = SpottiForm(request.POST or None, instance=spot)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'questions-form.html', {'form': form, 'spot': spot})

def delete_spot(request, id):
    spot = Skeittispotti.objects.get(id=id)

    if request.method == 'POST':
        spot.delete()
        return redirect('home')

    return render(request, 'q-delete-confirm.html', {'spot':spot})