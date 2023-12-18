from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Order
from collections import Counter

# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(request, 'shop/index.html', { 'products': products })

def cart(request):
    product_ids = ''
    
    if request.method == 'POST':
        if 'person' in request.POST:
            return process_order(request)
        elif 'product_ids' in request.POST:
            return display_cart(request)
        else:
            return HttpResponse('Неизвестный запрос')

def process_order(request):
    person = request.POST['person']
    address = request.POST['address']
    product_ids = request.POST['product_ids']

    try:
        all_products = get_products_from_ids(product_ids)
        if not all_products:
            raise Exception

        total_price, discount = calc_price_and_discount(all_products)

        create_order(person, address, discount, total_price, all_products)
        return success_order_response(person, total_price, discount)
    except:
        return HttpResponse(f"Неверно заполнена форма")

def get_products_from_ids(product_ids):
    all_products = []
    product_ids_list = [int(id) for id in product_ids.split(',') if id.strip().isdigit()]
    products = Product.objects.filter(id__in=product_ids_list)
    id_counts = Counter(product_ids_list)

    for product in products:
        count = id_counts[product.id]
        all_products.extend([product] * count)
    return all_products

def calc_price_and_discount(all_products):
    total_price = sum(product.price for product in all_products)
    unique_names = set(product.name for product in all_products)
    discount = 0

    if len(unique_names) > 1:
        discount = 10
        total_price -= total_price * (discount / 100)

    return total_price, discount

def create_order(person, address, discount, total_price, all_products):
    order = Order(person=person, address=address, discount=discount, price=total_price)
    order.save()
    order.products.set(all_products)
    return order

def success_order_response(person, total_price, discount):
    message = f"Ваш заказ оформлен. Спасибо, {person}! "
    if discount == 0:
        message += f"Итоговая цена {total_price}"
    else:
        message += f"Cо скидкой в {discount}% получится всего {total_price}"
    return HttpResponse(message)

def display_cart(request):
    product_ids = request.POST["product_ids"]
    all_products = get_products_from_ids(product_ids)
    
    context = {'products': all_products}
    return render(request, 'shop/cart.html', context)