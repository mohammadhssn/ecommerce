from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views import View


class ProductsAll(View):

    def get(self, request):
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)

        return render(request, 'store/home.html', {'products': products})


class ProductDetail(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)

        return render(request, 'store/product_detail.html', {'product': product})


class CategoryList(View):

    def get(self, request, category_slug=None):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True))

        return render(request, 'store/category.html', {'category': category, 'products': products})
