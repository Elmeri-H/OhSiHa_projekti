from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Skeittispotti
from .forms import SpottiForm
import requests
import json

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
        'spots' : spots,
    })

def show_chart1(request):
    response = requests.get(url)
    data = response.json()
    fielddata = data['result']
    fielddata = fielddata['records']
    cleanData = []
    yleiset_viheralueet = 0
    liikenne_viheralueet = 0
    kiinteistojen_viheralueet = 0


    for field in fielddata:
        if field['KAYTTOLK'] == 'LIIKENNEVIHERALUEET':
            liikenne_viheralueet += 1
        elif field['KAYTTOLK'] == 'YLEISET VIHERALUEET':
            yleiset_viheralueet += 1
        elif field['KAYTTOLK'] == 'KIINTEISTÖJEN VIHERALUEET':
            kiinteistojen_viheralueet += 1       


    yht = yleiset_viheralueet + liikenne_viheralueet + kiinteistojen_viheralueet
    
    chart = {
    'title': {
        'text': 'Alueiden<br>käyttöluokitukset',
        'align': 'center',
        'verticalAlign': 'middle',
        'y': 60
    },
    'tooltip': {
        'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    'accessibility': {
        'point': {
            'valueSuffix': '%'
        }
    },
    'plotOptions': {
        'pie': {
            'dataLabels': {
                'enabled': True,
                'distance': -50,
                'style': {
                    'fontWeight': 'bold',
                    'color': 'white'
                }
            },
            'startAngle': -90,
            'endAngle': 90,
            'center': ['50%', '75%'],
            'size': '110%'
        }
    },
    'series': [{
        'type': 'pie',
        'name': 'Osuus',
        'innerSize': '50%',
        'data': [
            ['Yleiset viheralueet', yleiset_viheralueet/yht],
            ['Liikenne viheralueet', liikenne_viheralueet/yht],
            ['Kiinteistöjen viheralueet', kiinteistojen_viheralueet/yht]
        ]
    }]
    }
    dump = json.dumps(chart)
    return render(request, 'chart1.html', {'chart' : dump})

def show_chart2(request):
    Iso_vilu = {
        'name' : 'Iso-Vilunen',
        'data' : [1271]
    }
    Tesoma = {
        'name' : 'Tesoma',
        'data' : [450]
    }
    Vapaa_ajan = {
        'name' : 'Vapaa-ajanmaan rullalautailualue',
        'data' : [1000]
    }
    Ratina = {
        'name' : 'Ratinan rullalautailupaikka',
        'data' : [100]
    }
    Kenneli = {
        'name' : 'Kenneli DIY',
        'data' : [1000]
    }
    chart = {
        'chart' : {'type':'column'},
        'title': {'text': 'Skeittipuistojen pinta-alat'},
        'series': [Iso_vilu, Tesoma, Vapaa_ajan, Ratina, Kenneli]
    }
    
    dump = json.dumps(chart)
    return render(request, 'chart2.html', {'chart' : dump})

def show_chart3(request):
    chart = {
        'chart' : {'type': 'timeline'},
        'xAxis': {
            'visible': False
        },
        'yAxis': {
            'visible': False
        },
        'title': {
        'text': 'Aikajana Tampereen skeittipuistoista lähivuosina.'
        },
        'subtitle': {
            'text': 'Aikajana on laadittu löytämieni tietojeni perusteella, eikä välttämättä kata kaikkia Tampereen skeittipuistoja ja -paikkoja.'
        },
        'colors': [
            '#4185F3',
            '#427CDD',
            '#406AB2',
            '#3E5A8E',
            '#3B4A68',
            '#363C46'
        ],
        'series': [{
            'data': [{
                'name': 'Iso-Vilusen skeittipusto valmistui.',
                'label': '2014: Tampereen suurin ja suosituin skeittipuisto valmistui loppuvuodesta.'
            }, {
                'name': 'Kaarikoirien skeittihalli avattiin',
                'label': '2017: Hiedanrannassa entisen tehdashallin tiloissa sijaitseva skeittihalli avattiin.'
            }, {
                'name': 'Hallilan skeittipaikan purku',
                'label': '2019: Hallilassa parkkipaikalla sijainnut pieni skeittipaikka purettiin ratikkatyömään tieltä.'
            }, {
                'name': 'Tikkutehdas DIY:n purku',
                'label': '2019: Tikkutehaan alueella sijainnut DIY-parkki purettiin uusien kerrostalojen tieltä.'
            }, {
                'name': 'Skeittihalli ABEC suljettiin',
                'label': '2019: Leinolassa toimineen skeittihallin toiminta lopetettiin yhteisymmärryksessä kaupungin kanssa, koska skeittitoiminta halutaan keskitettää Hiedanrantaan.'
            }, {
                'name': 'Kenneli DIY:n pihaparkki valmistui',
                'label': '2019: Loppusyksystä päästiin kokeilemaan pihaparkin uutta laajennusta.'
            }, {
                'name': 'Vapaa-ajanmaan rullalautailualueen purku',
                'label': '2020: Skeittipuisto purettiin uusien kerrostalojen tieltä.'
            }]
        }]
    }

    dump = json.dumps(chart)
    return render(request, 'chart3.html', {'chart' : dump})

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