from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator

from basket.basket import Basket
from orders.views import payment_confirmation
import stripe
import json


class BasketView(LoginRequiredMixin, View):
    def get(self, request):
        basket = Basket(request)
        total = str(basket.get_total_price())
        total = total.replace('.', '')
        total = int(total)

        stripe.api_key = 'sk_test_51K6LvrAditzYOocI1eVdxbGnM8byAMYLW7Pm92I0zkYVKgNIZYx3Wn23OFx5dZf19lmbYV5hzZkQHqvuOlUFPQD500mukpiWGe'
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={'userid': request.user.id}
        )

        return render(request, 'payment/home.html', {'client_secret': intent.client_secret})


class StripeWebhook(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            print(e)
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_confirmation(event.data.object.client_secret)

        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


class OrderPlaced(View):

    def get(self, request):
        basket = Basket(request)
        basket.clear()
        return render(request, 'payment/orderplaced.html')
