import openpyxl
from io import BytesIO
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *

def index(request):
    popular_products = Product.objects.all().order_by('-id')[:6]
    categories = Category.objects.all()
    
    context = {
        'popular_products': popular_products,
        'categories': categories
    }
    return render(request, 'shop/index.html', context)

def home(request):
    return render(request, 'home.html')

def about_author(request):
    return render(request, 'author.html')

def about_shop(request):
    return render(request, 'shop.html')

def product_list(request):
    products = Product.objects.all()

    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    search_query = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'catalog.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bucket, created = Bucket.objects.get_or_create(user=request.user)
    
    item, created = Bucket_Element.objects.get_or_create(
        bucket=bucket, 
        product=product, 
        defaults={'number': 1}
    )
    
   
    if not created:
        if item.number < product.stock_quantity:
            item.number += 1
            item.save()
        else:
            pass

    return redirect('cart_view')


def cart_update(request, item_id):
    item = get_object_or_404(Bucket_Element, id=item_id, bucket__user=request.user)
    new_number = int(request.POST.get('number', 0))
    
    if 0 < new_number <= item.product.stock_quantity:
        item.number = new_number
        item.save()
    
    return redirect('cart_view')


def cart_remove(request, item_id):
    item = get_object_or_404(Bucket_Element, id=item_id, bucket__user=request.user)
    item.delete()
    return redirect('cart_view')


def cart_view(request):
    bucket, created = Bucket.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'bucket': bucket})

@login_required
def checkout(request):
    return render(request, 'checkout.html')

def send_excel(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        address = request.POST.get('address')
        bucket = get_object_or_404(Bucket, user=request.user)
        items = bucket.bucket_element_set.all()

        if request.POST.get('need_receipt') and user_email:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(['Товар', 'Количество', 'Цена', 'Сумма'])

            total_sum = 0
            for item in items:
                cost = item.number * item.product.price
                ws.append([item.product.name, item.number, item.product.price, cost])
                total_sum += cost

            ws.append(['', '', 'Адрес:', address])
            ws.append(['', '', 'ИТОГО:', total_sum])

            buffer = BytesIO()
            wb.save(buffer)
            
            email = EmailMessage(
                'Ваш заказ', f'Доставка по адресу: {address}', 
                'noreply@test.com', [user_email]
            )
            email.attach('order.xlsx', buffer.getvalue(), 'application/vnd.ms-excel')
            email.send()

        items.delete()
        return redirect('cart_view')

    return redirect('cart_view')

from rest_framework import viewsets
from .serializers import *
from .models import * 

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GetterViewSet(viewsets.ModelViewSet):
    queryset = Getter.objects.all()
    serializer_class = GetterSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BucketViewSet(viewsets.ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer

class Bucket_ElementViewSet(viewsets.ModelViewSet):
    queryset = Bucket_Element.objects.all()
    serializer_class = Bucket_ElementSerializer