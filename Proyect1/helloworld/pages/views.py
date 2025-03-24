 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django.core.exceptions import ValidationError 
from django import forms
from .models import Product 

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            if image_url:
                request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View):
    template_name = 'images/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        if image_url:
            request.session['image_url'] = image_url
        return redirect('image_index')


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
    
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all()
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        #Revisar si es valido
        try:
            # Convertir el ID a entero
            product_id = int(id)
            # Verificar si el ID es válido
            if product_id < 1:
                raise ValueError("El ID de producto debe ser 1 o mayor")
            product = get_object_or_404(Product, pk=product_id)
            #return HttpResponseRedirect(reverse('home'))  # Redirige a la página de inicio
        except (ValueError, IndexError):
            # Si el ID no es un número o está fuera de rango, redirigir al home
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product 

        return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    cotext_object_name = 'products' # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context 


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    # Validación personalizada para que el precio sea mayor a 0
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("The price must be greater than zero.")  
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
            form.save()
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

class CartView(View): 
    template_name = 'cart/index.html' 
     
    def get(self, request): 
        # Simulated database for products 
        products = {} 
        products[121] = {'name': 'Tv samsung', 'price': '1000'} 
        products[11] = {'name': 'Iphone', 'price': '2000'} 
 
        # Get cart products from session 
        cart_products = {} 
        cart_product_data = request.session.get('cart_product_data', {}) 
 
        for key, product in products.items(): 
            if str(key) in cart_product_data.keys(): 
                cart_products[key] = product 
 
        # Prepare data for the view 
        view_data = { 
            'title': 'Cart - Online Store', 
            'subtitle': 'Shopping Cart', 
            'products': products, 
            'cart_products': cart_products 
        } 
 
        return render(request, self.template_name, view_data)
    
    def post(self, request, product_id): 
        # Get cart products from session and add the new product 
        cart_product_data = request.session.get('cart_product_data', {}) 
        cart_product_data[product_id] = product_id 
        request.session['cart_product_data'] = cart_product_data 

        return redirect('cart_index')
 
 
class CartRemoveAllView(View): 
    def post(self, request): 
        # Remove all products from cart in session 
        if 'cart_product_data' in request.session: 
            del request.session['cart_product_data'] 
 
        return redirect('cart_index')
    
