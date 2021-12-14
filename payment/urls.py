from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView.as_view(), name='basket'),
    path('orderplaced/', views.OrderPlaced.as_view(), name='order_placed'),
    path('webhook/', views.StripeWebhook.as_view()),
]
