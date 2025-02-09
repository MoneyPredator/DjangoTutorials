 
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView 
from django.views import View
from django.urls import reverse
from django.core.exceptions import ValidationError 
from django import forms
# Create your views here. 
class HomePageView(TemplateView): 
    template_name = 'pages/home.html' 
 
 
 
class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
 
        return context 
    
 
class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 500.00},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999.99},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 35.50},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 80.75}
    ]
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            # Convertir el ID a entero
            product_id = int(id)

            # Verificar si el ID es válido
            if product_id < 1 or product_id > len(Product.products):
                return HttpResponseRedirect(reverse('home'))  # Redirige a la página de inicio

            product = Product.products[product_id - 1]
            viewData = {
                "title": f"{product['name']} - Online Store",
                "subtitle": f"{product['name']} - Product information",
                "product": product,
            }
            return render(request, self.template_name, viewData)

        except (ValueError, IndexError):
            # Si el ID no es un número o está fuera de rango, redirigir al home
            return HttpResponseRedirect(reverse('home'))

    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    # Validación personalizada para que el precio sea mayor a 0
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("The price must be greater than zero.")  # Mensaje de error
        return price
 
 
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect('home')  # Redirigir a la página de inicio tras el envío
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "sacardenal@eafit.edu.com",
            "address": "Universidad EAFIT, Clase Topicos, MDE",
            "phone": "+123 456 7890",
        })
        return context
