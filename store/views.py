from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views import View


class ProductsAll(View):

    def get(self, request):
        products = Product.products.all()

        return render(request, 'store/home.html', {'products': products})


class ProductDetail(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, in_stock=True)

        return render(request, 'store/product_detail.html', {'product': product})


class CategoryList(View):

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

        return render(request, 'store/category.html', {'category': category, 'products': products})
