from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from basket.basket import Basket
import stripe


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
