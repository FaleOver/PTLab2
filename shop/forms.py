from django.forms import HiddenInput, ModelForm, TextInput
from .models import Product, Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['person', 'address', 'products']
        
        widgets = {
            'products': HiddenInput(),
            'person': TextInput(attrs={
                'class': 'input',
                'placeholder': 'ФИО'
                }),
            'address': TextInput(attrs={
                'class': 'input',
                'placeholder': 'АДРЕС'
                })
            }