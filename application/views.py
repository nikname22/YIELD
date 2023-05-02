from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import pandas as pd
import requests
from .models import Project
from geopy.geocoders import Nominatim
import yfinance as yf
stock_selected = ''
period_selected = ''

def home(request):      
    input_filter = request.POST.get('filter_project')
    if input_filter:
        projects = Project.objects.filter(projeto__icontains = input_filter)
    else:
        projects = Project.objects.all()

    project_paginator = Paginator(projects, 6)
    page_num = request.GET.get('page')
    page = project_paginator.get_page(page_num)
    return render(request,'pages/home.html', {'page': page})

def page_create(request):
     return render(request,'pages/create_project.html')

def populate_database(request):
    responses = requests.get('https://urbe.me/administracao/api/lista-projetos/').json()    
    for response in responses:        
        new_project = Project()            
        new_project.projeto = response['projeto']
        new_project.latitude = response['latitude']
        new_project.longitude = response['longitude']
        new_project.tir_media = response['tir_media']
        new_project.total_captado = response['total_captado']
        new_project.vgv = response['vgv']
        new_project.save() 
    return redirect(home)       

def delete_database(request):
    project = Project.objects.all()
    project.delete()
    return redirect(home)    

def create(request):    
    new_project = Project()    
    new_project.projeto = request.POST.get('projeto')
    new_project.latitude = request.POST.get('latitude')
    new_project.longitude = request.POST.get('longitude')
    new_project.tir_media = request.POST.get('tir_media')
    new_project.total_captado = request.POST.get('total_captado')
    new_project.vgv = request.POST.get('vgv')
    new_project.save()       
    return redirect(home)

def edit(request, id):    
    project = Project.objects.get(id_project=id)
    return render(request,'pages/update.html', {"project": project})

def update(request,id):
     project = Project.objects.get(id_project=id)
     project.projeto = request.POST.get('projeto')
     project.latitude = request.POST.get('latitude')
     project.longitude = request.POST.get('longitude')
     project.tir_media = request.POST.get('tir_media')
     project.total_captado = request.POST.get('total_captado')
     project.vgv = request.POST.get('vgv')
     project.save()    
     return redirect(home)   

def delete(request, id):
    project = Project.objects.get(id_project=id)
    project.delete()    
    return redirect(home)

def compare(request, id):    
    project = Project.objects.get(id_project=id)   
    latitude = project.latitude
    longitude = project.longitude  
    tickers=['ABEV3','BOVA11','HGLG11','IVVB11','ITUB3','PETR4','TAEE11']
    periods=['1 mês', '1 ano', '5 anos']
    start_period = ''
    end_period = ''
    data = ''
    time_value = ''

    if period_selected == '1 mês':
        time_value = '1mo'
    elif period_selected == '1 ano':
        time_value = '1y'
    else:
        time_value = '5y'

    if stock_selected != '':
        ticker = [f"{stock_selected}.SA"]    
        search_data = yf.download(ticker,period=f"{time_value}")['Adj Close']  
        start_period = search_data.index[0].date().strftime("%d/%m/%Y")
        end_period = search_data.index[-1].date().strftime("%d/%m/%Y")        
        data = ((search_data[-1]/search_data[0]) -1) * 100        

    if latitude is not None and longitude is not None:
        geolocator = Nominatim(user_agent="user_agent") 
        location = geolocator.reverse(f"{latitude}, {longitude}")          
        address = f"{location.address.split(',')[0]}, {location.address.split(',')[2]}, {location.address.split(',')[4]}, {location.address.split(',')[-4]}"       
    return render(request,'pages/compare.html', {
        "project": project, 
        "address": address, 
        'stock_selected': stock_selected, 
        'period_selected': period_selected,
        'tickers': tickers,
        'periods': periods,
        'start_period': start_period,
        'end_period': end_period,
        'data': data,
    })

def compare_stock(request, id):
    project = Project.objects.get(id_project=id)
    global stock_selected    
    global period_selected
    stock_selected = request.GET['stock_selector']    
    period_selected = request.GET['period_selector']    
    return redirect('compare', id=project.id_project)