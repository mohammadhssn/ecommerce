from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .basket import Basket
from catalogue.models import Product


class BasketSummary(View):

    def get(self, request):
        basket = Basket(request)
        return render(request, 'basket/basket_summary.html', {'basket': basket})


class BasketAdd(View):

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


class BasketDelete(View):

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


class BasketUpdate(View):

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
