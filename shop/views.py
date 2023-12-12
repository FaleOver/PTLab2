from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Order
from django.db.models import Sum
import json
from django.views.decorators.csrf import csrf_protect
from collections import Counter
from .forms import OrderForm

# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(request, 'shop/index.html', { 'products': products })

def cart(request):
    product_ids = ''
    
    if request.method == 'POST':
        if request.POST.get('person'):
            person = request.POST['person']
            address = request.POST['address']
            product_ids = request.POST['product_ids']

            try:
                all_products = ids_to_products(product_ids)
                if not all_products: raise Exception
                order = Order(person=person, address=address)
                order.save()
                order.products.set(all_products)
                cost = sum(product.price for product in all_products)
                cost_with_discount = cost * 0.9
                return HttpResponse("Ваш заказ оформлен. Спасибо, {0}! Сумма составляет {1:.2f}, ".format(person, cost) +
                                    "но со скидкой получится всего {0:.2f}".format(cost_with_discount))
            except:
                return HttpResponse(f"Неверно заполнена форма")
        elif request.POST.get('product_ids'):
            product_ids = request.POST["product_ids"]
            all_products = ids_to_products(product_ids)
            
            context = {
                'products': all_products
                }
            return render(request, 'shop/cart.html', context)
        else:
            return HttpResponse('Неизвестный запрос')

def ids_to_products(product_ids):
    all_products = []
    product_ids_list = [int(id) for id in product_ids.split(',') if id.isdigit()]
    products = Product.objects.filter(id__in=product_ids_list)
    # Создаем список продуктов, включая дубликаты в соответствии с количеством повторений
    # Создаем словарь, в котором ключи - это идентификаторы, а значения - количество повторений
    id_counts = Counter(product_ids_list)
        
    for product in products:
        count = id_counts[product.id]
        all_products.extend([product] * count)
    return all_products

# class PurchaseCreate(CreateView):
#     model = Purchase
#     fields = ['product', 'person', 'address']

#     def form_valid(self, form):
#         self.object = form.save()
#         return HttpResponse(f'Спасибо за покупку, { self.object.person }!')