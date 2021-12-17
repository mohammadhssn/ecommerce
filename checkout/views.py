from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages

from .models import DeliveryOptions

from account.models import Address
from basket.basket import Basket


class DeliveryChoices(LoginRequiredMixin, View):

    def get(self, request):
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
        return render(request, 'checkout/delivery_choices.html', {'deliveryoptions': deliveryoptions})


class BasketUpdateDelivery(LoginRequiredMixin, View):

    def post(self, request):
        basket = Basket(request)
        delivery_option = int(request.POST.get('deliveryoption'))
        delivery_type = get_object_or_404(DeliveryOptions, id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': delivery_type.id,
            }
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        response = JsonResponse({'total': updated_total_price, 'delivery_price': delivery_type.delivery_price})
        return response


class DeliveryAddress(LoginRequiredMixin, View):

    # def dispatch(self, request, *args, **kwargs):
    #     previous_url = request.META.get('HTTP_REFERER')
    #
    #     if previous_url is None:
    #         return redirect('store:store_home')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        session = request.session
        if 'purchase' not in request.session:
            messages.success(request, 'Please select delivery option')
            try:
                return redirect(request.META.get('HTTP_REFERER'))
            except TypeError:
                return redirect('store:store_home')

        addresses = Address.objects.filter(customer=request.user).order_by('-default')
        if addresses:
            if 'address' not in request.session:
                session['address'] = {'address_id': str(addresses[0].id)}
            else:
                session['address']['address_id'] = str(addresses[0].id)
                session.modified = True

        return render(request, 'checkout/delivery_address.html', {'addresses': addresses})


class PaymentSelection(LoginRequiredMixin, View):

    # def dispatch(self, request, *args, **kwargs):
    #     previous_url = request.META.get('HTTP_REFERER')
    #
    #     if previous_url is None:
    #         return redirect('store:store_home')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        session = request.session
        if 'address' not in request.session:
            messages.success(request, 'Please select address option')
            try:
                return redirect(request.META.get('HTTP_REFERER'))
            except TypeError:
                return redirect('store:store_home')

        return render(request, 'checkout/payment_selection.html')
