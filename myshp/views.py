from django.shortcuts import render

def hello_world(request):
    return render(request, 'index.html')

def author(request):
    return render(request, 'index_auther.html')

def shop(request):
    return render(request, 'index_shop.html')