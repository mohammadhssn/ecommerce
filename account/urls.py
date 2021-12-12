from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.AccountRegister.as_view(), name='register'),
    path('login/', views.AccountLogin.as_view(), name='login'),
    path('logout/', views.AccountLogout.as_view(), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.AccountActivate.as_view(), name='activate'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
]
